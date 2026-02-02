import { useState } from "react";
import SupportModal from "../components/Payment/SupportModal";

export default function DummyPage() {
  const [isSupportOpen, setIsSupportOpen] = useState(false);
  const [users] = useState([
    { id: 1, name: "John Doe", email: "john@email.com", status: "Active" },
    { id: 2, name: "Sarah Smith", email: "sarah@email.com", status: "Pending" },
    { id: 3, name: "Mike Ross", email: "mike@email.com", status: "Blocked" },
  ]);
  const creator = {
    user: {
      id: 5,
      email: "user1@gmail.com",
      username: "user1",
      first_name: "",
      last_name: "",
      user_type: "creator",
      is_active: true,
      date_joined: "2026-01-30T22:42:46.829471+02:00",
      slug: "user1",
    },
    bio: "",
    profile_image: null,
    website: "",
    followers_count: 0,
    rating: 5.0,
    verified: false,
    created_at: "2026-01-30T23:37:28.178097+02:00",
    updated_at: "2026-01-30T23:37:28.178144+02:00",
  };

  return (
    <div style={styles.page}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.title}>Dashboard</h1>
        <button style={styles.button}>+ Add User</button>
      </header>

      {/* Cards Section */}
      <div style={styles.cardContainer}>
        <div style={styles.card}>
          <h3>Total Users</h3>
          <p style={styles.cardNumber}>128</p>
        </div>
        <div style={styles.card}>
          <h3>Active</h3>
          <p style={styles.cardNumber}>102</p>
        </div>
        <div style={styles.card}>
          <h3>Pending</h3>
          <p style={styles.cardNumber}>18</p>
        </div>
        <div style={styles.card}>
          <h3>Blocked</h3>
          <p style={styles.cardNumber}>8</p>
        </div>
      </div>

      {/* Table */}
      <div style={styles.tableWrapper}>
        <h2>Recent Users</h2>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Name</th>
              <th style={styles.th}>Email</th>
              <th style={styles.th}>Status</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td style={styles.td}>{user.name}</td>
                <td style={styles.td}>{user.email}</td>
                <td style={styles.td}>
                  <span
                    style={{
                      ...styles.status,
                      backgroundColor:
                        user.status === "Active"
                          ? "#d4edda"
                          : user.status === "Pending"
                            ? "#fff3cd"
                            : "#f8d7da",
                      color:
                        user.status === "Active"
                          ? "#155724"
                          : user.status === "Pending"
                            ? "#856404"
                            : "#721c24",
                    }}
                  >
                    {user.status}
                    <button onClick={() => setIsSupportOpen(true)}>
                      Send a Tip
                    </button>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <SupportModal
        isOpen={isSupportOpen}
        onClose={() => setIsSupportOpen(false)}
        creator={{
          id: creator?.user?.id,
          name: creator?.user?.username,
        }}
      />
    </div>
  );
}

const styles = {
  page: {
    fontFamily: "Arial, sans-serif",
    padding: "30px",
    backgroundColor: "#f5f7fa",
    minHeight: "100vh",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
  },
  title: {
    margin: 0,
  },
  button: {
    padding: "10px 16px",
    backgroundColor: "#4f46e5",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  cardContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "20px",
    marginBottom: "30px",
  },
  card: {
    backgroundColor: "white",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
  },
  cardNumber: {
    fontSize: "24px",
    fontWeight: "bold",
    marginTop: "10px",
  },
  tableWrapper: {
    backgroundColor: "white",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "10px",
  },
  th: {
    textAlign: "left",
    padding: "10px",
    borderBottom: "2px solid #eee",
  },
  td: {
    padding: "10px",
    borderBottom: "1px solid #eee",
  },
  status: {
    padding: "4px 10px",
    borderRadius: "12px",
    fontSize: "12px",
    fontWeight: "bold",
  },
};
