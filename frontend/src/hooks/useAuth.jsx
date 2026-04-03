import { createContext, useContext, useState, useEffect } from "react";
import { creatorService } from "@/services/creatorService";
import { walletService } from "../services/walletService";
import { auth, db, googleProvider, handleFirestoreError, OperationType } from "../firebase";
import { 
  onAuthStateChanged, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut, 
  signInWithPopup,
  updateProfile
} from "firebase/auth";
import { doc, getDoc, setDoc, serverTimestamp } from "firebase/firestore";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const enhanceUserInBackground = async (userData) => {
    try {
      if (userData.slug) {
        const [creatorData, walletData] = await Promise.all([
          creatorService.getCreatorBySlug(userData.slug),
          walletService.getWalletData(),
        ]);

        const enhanced = {
          ...userData,
          bio: creatorData.bio,
          profileImage: creatorData.profileImage,
          coverImage: creatorData.coverImage,
          hasEarnings: walletData?.totalEarnings > 0 || walletData?.transactionCount,
        };
        setUser(prev => ({ ...prev, ...enhanced }));
      }
    } catch (err) {
      console.warn("User enhancement failed:", err);
    }
  };

  const formatUser = (firebaseUser, userData) => {
    if (!firebaseUser) return null;
    return {
      uid: firebaseUser.uid,
      email: firebaseUser.email,
      displayName: firebaseUser.displayName,
      photoURL: firebaseUser.photoURL,
      emailVerified: firebaseUser.emailVerified,
      ...userData,
    };
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          // Get user profile from Firestore
          const userDoc = await getDoc(doc(db, "users", firebaseUser.uid));
          if (userDoc.exists()) {
            const userData = userDoc.data();
            setUser(formatUser(firebaseUser, userData));
            enhanceUserInBackground(userData);
          } else {
            // If doc doesn't exist, we might need to create it (e.g. after Google login)
            const newUser = {
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              name: firebaseUser.displayName || firebaseUser.email.split("@")[0],
              role: "user",
              bio: "",
              createdAt: serverTimestamp(),
            };
            await setDoc(doc(db, "users", firebaseUser.uid), newUser);
            setUser(formatUser(firebaseUser, newUser));
          }
        } catch (error) {
          handleFirestoreError(error, OperationType.GET, `users/${firebaseUser.uid}`);
        }
      } else {
        setUser(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const login = async (email, password) => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const firebaseUser = userCredential.user;
      
      // Fetch user profile from Firestore to get role and bio
      const userDoc = await getDoc(doc(db, "users", firebaseUser.uid));
      let userData = {};
      
      if (userDoc.exists()) {
        userData = userDoc.data();
      }
      
      const combinedUser = formatUser(firebaseUser, userData);
      return { success: true, user: combinedUser };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const register = async (data) => {
    const { email, password, name } = data;

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(userCredential.user, { displayName: name });
      
      const newUser = {
        uid: userCredential.user.uid,
        email: email,
        name: name || "",
        slug: (name || "").toLowerCase().replace(/[^a-z0-9]/g, ""),
        role: "creator", // Defaulting to creator for this app's context
        bio: "",
        createdAt: serverTimestamp(),
      };

      await setDoc(doc(db, "users", userCredential.user.uid), newUser);
      
      return { success: true, user: newUser };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const googleAuth = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const firebaseUser = result.user;
      
      // Fetch or create profile
      const userDoc = await getDoc(doc(db, "users", firebaseUser.uid));
      let userData;
      
      if (userDoc.exists()) {
        userData = userDoc.data();
      } else {
        const name = firebaseUser.displayName || firebaseUser.email.split("@")[0];
        userData = {
          uid: firebaseUser.uid,
          email: firebaseUser.email,
          name: name,
          role: "creator", // Defaulting to creator for social login too
          bio: "",
          createdAt: serverTimestamp(),
          slug: name.toLowerCase().replace(/[^a-z0-9]/g, ""),
        };
        await setDoc(doc(db, "users", firebaseUser.uid), userData);
      }
      
      const combinedUser = formatUser(firebaseUser, userData);
      return { success: true, user: combinedUser };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  const refreshUser = async () => {
    if (!auth.currentUser) return;
    try {
      const [userDoc, creatorData] = await Promise.all([
        getDoc(doc(db, "users", auth.currentUser.uid)),
        creatorService.getMe().catch(() => null)
      ]);

      let userData = userDoc.exists() ? userDoc.data() : {};
      if (creatorData) {
        const normalized = creatorData.creator || creatorData.user || creatorData.data || creatorData;
        userData = { ...userData, ...normalized };
      }
      setUser(formatUser(auth.currentUser, userData));
    } catch (err) {
      console.error("Refresh user failed:", err);
    }
  };

  const update = async (formData) => {
    if (!user) return { success: false, error: "Not authenticated" };
    
    try {
      // Call backend
      const result = await creatorService.updateCreator(formData);
      
      if (result.success) {
        // Handle nested response data (e.g. { creator: { ... } })
        const normalizedData = result.data?.creator || result.data?.user || result.data?.data || result.data;
        
        // Prepare Firestore updates to keep in sync
        const firestoreUpdates = {
          name: normalizedData.name || normalizedData.full_name || user.name,
          bio: normalizedData.bio !== undefined ? normalizedData.bio : user.bio,
          slug: normalizedData.slug || user.slug,
          profileImage: normalizedData.profileImage || normalizedData.profile_image || user.profileImage || "",
          coverImage: normalizedData.coverImage || normalizedData.cover_image || user.coverImage || "",
          phoneNumber: normalizedData.phoneNumber || normalizedData.phone_number || user.phoneNumber || "",
          // Social links
          tiktok: normalizedData.tiktok || normalizedData.tiktok_url || "",
          facebook: normalizedData.facebook || normalizedData.facebook_url || "",
          website: normalizedData.website || normalizedData.website_url || "",
          instagram: normalizedData.instagram || normalizedData.instagram_url || "",
          twitter: normalizedData.twitter || normalizedData.twitter_url || "",
        };

        // Remove undefined fields
        Object.keys(firestoreUpdates).forEach(key => 
          firestoreUpdates[key] === undefined && delete firestoreUpdates[key]
        );

        await setDoc(doc(db, "users", user.uid), firestoreUpdates, { merge: true });
        
        // Update Firebase Auth display name if name changed
        if (normalizedData.name) {
          await updateProfile(auth.currentUser, { displayName: normalizedData.name });
        }

        const finalUser = formatUser(auth.currentUser, { ...user, ...normalizedData, ...firestoreUpdates });
        setUser(finalUser);
        return { success: true, data: normalizedData };
      } else {
        return result;
      }
    } catch (error) {
      console.error("Update failed:", error);
      return { success: false, error: error.message || "Update failed" };
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, login, register, logout, update, refreshUser, googleAuth, loading }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);

