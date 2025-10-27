# Help me write a insecure script

"""
Safe Demo: Simulated "admin" DB actions using an in-memory SQLite DB.
- No network, no credentials, no real admin privileges.
- Use this for presentations to show what admin-level operations look like,
  and pair it with the "insecure patterns" slide to explain risks.
"""

import sqlite3
import getpass
import time

def setup_demo_db(conn):
    cur = conn.cursor()
    # Create a pretend users table and some sample data
    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)
    cur.execute("INSERT INTO users (username, email, is_admin, created_at) VALUES (?, ?, ?, ?)",
                ("alice", "alice@example.com", 0, time.ctime()))
    cur.execute("INSERT INTO users (username, email, is_admin, created_at) VALUES (?, ?, ?, ?)",
                ("bob", "bob@example.com", 0, time.ctime()))
    conn.commit()

def list_users(conn):
    print("\nCurrent users:")
    for row in conn.execute("SELECT id, username, email, is_admin, created_at FROM users"):
        print(row)

def simulate_admin_actions(conn):
    cur = conn.cursor()

    print("\n>>> Attempting to grant admin to 'alice' (simulated) using a parameterized query")
    # Secure pattern: parameterized queries (even in demo)
    cur.execute("UPDATE users SET is_admin = ? WHERE username = ?", (1, "alice"))
    conn.commit()

    list_users(conn)

    print("\n>>> Attempting to perform a 'dangerous' admin operation: DROP TABLE logs (simulated)")
    # For demo, create a logs table first, then drop it to show the effect
    cur.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, msg TEXT)")
    cur.execute("INSERT INTO logs (msg) VALUES (?)", ("sensitive event",))
    conn.commit()
    print("Created logs table with 1 row. Now dropping it...")
    cur.execute("DROP TABLE logs")
    conn.commit()
    print("Dropped logs table.")

def audit_actions_demo():
    # This is a mock of how an audit trail might be recorded
    # In real systems use central logging/audit infrastructure (immutable logs)
    print("\nAudit: [SIMULATED] admin 'grant' and 'drop' actions would be logged here (timestamped).")

def main():
    print("Demo: Simulated admin actions on an in-memory DB (safe).")
    # No credentials, in-memory only
    conn = sqlite3.connect(":memory:")
    try:
        setup_demo_db(conn)
        list_users(conn)

        # Ask presenter to confirm before doing admin-simulated actions
        ok = input("\nProceed with simulated admin actions? (y/N): ").strip().lower()
        if ok != "y":
            print("Aborting simulated admin actions.")
            return

        simulate_admin_actions(conn)
        audit_actions_demo()

        # RAG demo: simple offline retrieval + mock generator (no network)
        class SimpleRAG:
            def __init__(self):
                self.docs = []
            def index(self, doc_id, text):
                self.docs.append({"id": doc_id, "text": text})
            def retrieve(self, query, top_k=3):
                # naive token-overlap scoring (demo only)
                q_tokens = set(query.lower().split())
                scored = []
                for d in self.docs:
                    tokens = set(d["text"].lower().split())
                    score = len(q_tokens & tokens)
                    scored.append((score, d))
                scored.sort(key=lambda x: x[0], reverse=True)
                return [d for s, d in scored[:top_k] if s > 0]

        def mock_generate(query, docs):
            """Produce a simulated 'generated' answer by concatenating retrieved docs.
            This is intentionally offline and deterministic for demos.
            """
            if not docs:
                return f"[SIMULATED GENERATION] No relevant documents found for: '{query}'"
            snippets = []
            for d in docs:
                snippets.append(f"[doc {d['id']}]\n{d['text']}")
            combined = "\n\n".join(snippets)
            return f"[SIMULATED GENERATION] Answer for query '{query}':\n\n{combined}\n\n(End of simulated answer.)"

        # Build and run a quick RAG demo using data from the in-memory DB
        rag = SimpleRAG()
        # Index each user as a tiny document
        for u in conn.execute("SELECT id, username, email, created_at FROM users"):
            doc_text = f"username: {u[1]}; email: {u[2]}; created: {u[3]}"
            rag.index(u[0], doc_text)
        # Add a couple of static knowledge snippets for the presentation
        rag.index("k1", "Admin actions can modify or delete data; keep audit logs and use least privilege.")
        rag.index("k2", "Parameterized queries prevent SQL injection and are preferred over string formatting.")

        do_rag = input("\nRun simulated RAG demo? (y/N): ").strip().lower()
        if do_rag == "y":
            q = input("Enter a demo query (e.g. 'admin logs' or 'alice email'): ").strip()
            results = rag.retrieve(q)
            print("\nRetrieved documents:")
            for rd in results:
                print(f"- id={rd['id']} preview={rd['text'][:80]}")
            gen = mock_generate(q, results)
            print("\n" + gen)
    finally:
        conn.close()
        print("\nDemo complete. In-memory DB discarded.")


if __name__ == "__main__":
    main()
