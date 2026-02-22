# Push from this environment to GitHub (secure, one-time setup)

This guide makes **git push** work from Cursor/your machine **without typing credentials every time**. Credentials are stored securely by the system (macOS Keychain or GitHub CLI), not in the repo or in code.

---

## One-time setup (choose one method)

### Option 1: Git + macOS Keychain (recommended on Mac)

1. **Create a GitHub Personal Access Token (PAT)**  
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic).  
   - Generate new token (classic); check **repo** scope; set expiry (e.g. 90 days or 6 months).  
   - Copy the token once (you won’t see it again).

2. **Tell Git to store credentials in Keychain** (once per machine):
   ```bash
   git config --global credential.helper osxkeychain
   ```

3. **First push from this repo** (you’ll be prompted once):
   ```bash
   cd /Users/simha/code/dqm-framework
   git remote set-url origin https://github.com/YOUR_USERNAME/dqm-framework.git   # if needed
   git push -u origin main
   ```
   - **Username:** your GitHub username.  
   - **Password:** paste your **PAT** (not your GitHub account password).  
   After this, the PAT is stored in Keychain and future pushes from this environment work without prompts.

4. **Later:** Any time you run `git push` (or the script below) from this repo, Git will use the stored credentials. No need to enter them again until the PAT expires or you revoke it.

---

### Option 2: GitHub CLI (gh)

1. **Install GitHub CLI** (if needed):  
   `brew install gh`

2. **Log in once** (stores token securely):
   ```bash
   gh auth login
   ```
   Follow the prompts (GitHub.com, HTTPS or SSH, authenticate in browser or with PAT).

3. **Push** from the repo:
   ```bash
   cd /Users/simha/code/dqm-framework
   git push -u origin main
   ```
   Future pushes work without re-entering credentials.

---

### Option 3: SSH key

1. **Generate an SSH key** (if you don’t have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_github
   ```

2. **Add the public key to GitHub**  
   - Copy `~/.ssh/id_ed25519_github.pub` and add it in GitHub → Settings → SSH and GPG keys.

3. **Use SSH remote** (no password after key is added):
   ```bash
   cd /Users/simha/code/dqm-framework
   git remote set-url origin git@github.com:YOUR_USERNAME/dqm-framework.git
   git push -u origin main
   ```

---

## After one-time setup: push from this environment

- **From terminal (Cursor or any shell):**
  ```bash
  cd /Users/simha/code/dqm-framework
  git add -A
  git commit -m "Your message"
  git push origin main
  ```
- **Or use the helper script:**
  ```bash
  ./scripts/push_to_github.sh
  ```
  (Script only runs `git push`; you still commit locally when you want.)

No credentials are stored in the repo or in scripts; they stay in Keychain (Option 1), GitHub CLI (Option 2), or your SSH agent (Option 3).

---

## Using this repo in Databricks

1. **Push from here** to GitHub (using the setup above).  
2. In **Databricks**: Repos → Add Repo → paste your GitHub repo URL, authenticate (PAT or GitHub App).  
3. Open the repo in Databricks and set branch to **main**.  
4. Create jobs that run `Universal_Execution_Script` from the Repo path; set the task’s **source to Git** and branch **main**.

The framework “lives” in Databricks by cloning this repo; you keep developing in Cursor and push changes to GitHub, and Databricks uses the latest code from GitHub.
