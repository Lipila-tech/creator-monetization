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
      // This part depends on the existing creatorService which might still point to the old backend
      // If the user wants full Firebase, we might need to migrate these services too.
      // For now, I'll keep it but wrap in try-catch.
      if (userData.slug) {
        const [{ data: creatorData }, walletData] = await Promise.all([
          creatorService.getCreatorBySlug(userData.slug),
          walletService.getWalletData(),
        ]);

        const enhanced = {
          ...userData,
          bio: creatorData.bio,
          profileImage: creatorData.profileImage || userData.photoURL,
          coverImage: creatorData.coverImage,
          hasEarnings: walletData?.totalEarnings > 0 || walletData?.transactionCount,
        };
        setUser(prev => ({ ...prev, ...enhanced }));
      }
    } catch (err) {
      console.warn("User enhancement failed:", err);
    }
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          // Get user profile from Firestore
          const userDoc = await getDoc(doc(db, "users", firebaseUser.uid));
          if (userDoc.exists()) {
            const userData = userDoc.data();
            setUser({
              ...firebaseUser,
              ...userData,
            });
            enhanceUserInBackground(userData);
          } else {
            // If doc doesn't exist, we might need to create it (e.g. after Google login)
            const newUser = {
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              displayName: firebaseUser.displayName,
              photoURL: firebaseUser.photoURL,
              role: "user",
              createdAt: serverTimestamp(),
            };
            await setDoc(doc(db, "users", firebaseUser.uid), newUser);
            setUser(newUser);
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
      return { success: true, user: userCredential.user };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const register = async (data) => {
    const { email, password, firstName, lastName, username } = data;
    const displayName = `${firstName || ""} ${lastName || ""}`.trim() || username;

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(userCredential.user, { displayName });
      
      const newUser = {
        uid: userCredential.user.uid,
        email: email,
        displayName: displayName,
        username: username || "",
        role: "creator", // Defaulting to creator for this app's context
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
      return { success: true, user: result.user };
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

  const update = async (formData) => {
    if (!user) return { success: false, error: "Not authenticated" };
    
    try {
      const updates = {};
      if (formData.get("display_name")) updates.displayName = formData.get("display_name");
      if (formData.get("bio")) updates.bio = formData.get("bio");
      
      await setDoc(doc(db, "users", user.uid), updates, { merge: true });
      setUser(prev => ({ ...prev, ...updates }));
      
      return { success: true };
    } catch (error) {
      handleFirestoreError(error, OperationType.UPDATE, `users/${user.uid}`);
      return { success: false, error: error.message };
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, login, register, logout, update, googleAuth, loading }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);
