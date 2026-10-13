# Running Containers Safely — 3 Simple Rules

This lecture adds three small things to the Dockerfile:

1. **Don't run the app as the admin (root) user.** Make a normal user and use that.
2. **Tell Docker which port the app uses** with `EXPOSE`.
3. **Pass settings from outside** with environment variables, instead of hard-coding them.

That's it. Each one is explained below with a tiny example.

---

## 1. Don't run as root

### The problem, in plain words

Inside a container there is a user called **root**. Root is the admin. Root can delete
anything and change anything.

By default, your app runs as root. So if someone finds a bug in your app and gets in,
**they are the admin**. That's dangerous.

### The fix: make a normal user and switch to it

Think of it like a laptop. You don't do daily work logged in as the admin. You make a
normal account and use that.

```dockerfile
RUN addgroup --gid 1001 nodejs                                   # make a group
RUN adduser --uid 1001 --ingroup nodejs --disabled-password nodejs   # make a user in it
USER nodejs                                                      # switch to that user
CMD ["npm", "start"]                                             # now runs as nodejs, not root
```

| Line | In plain words |
|---|---|
| `addgroup ... nodejs` | create a group called `nodejs` |
| `adduser ... nodejs` | create a user called `nodejs` |
| `USER nodejs` | from here on, everything runs as `nodejs` |

### Why a group AND a user, with the same name and number?

| Line | Creates | Name | Number |
|---|---|---|---|
| `addgroup --gid 1001 nodejs` | a **group** | `nodejs` | group id 1001 |
| `adduser --uid 1001 --ingroup nodejs ... nodejs` | a **user** | `nodejs` | user id 1001 |

- **Why both?** In Linux every user must belong to a group. Think team and member: make
  the team, then add the person to it. `--ingroup nodejs` puts the user in the group.
- **Why the same name and number?** Convenience only. Nothing forces it. Same name and
  same id are easy to remember and easy to spot in file listings (`nodejs nodejs`).
  `addgroup --gid 2000 appteam` + `adduser --uid 1001 --ingroup appteam bob` works too.
- **Why 1001?** Ids under 1000 are reserved for system accounts. 1000 is usually the first
  normal user. 1001 is just the next free one. Anything from 1000 up is fine.

**Where to put it:** near the **end** of the Dockerfile, after `npm install`, right before
`CMD`. Installing needs admin. Running the app does not.

**Check it worked:**

```bash
docker exec -it <container> whoami
```

```text
nodejs        ← good. If it says root, the USER line is missing or in the wrong place
```

---

## 2. Tell Docker the port

```dockerfile
EXPOSE 8000
```

This is a **label**. It says "this app listens on 8000". It does **not** open the port by
itself. You still run with `-p 8000:8000`.

---

## 3. Pass settings from outside (environment variables)

### What an environment variable is

A **named value** the app reads when it starts. In the code: `process.env.PORT`.
Why? So the same image can run on port 8000 today and 3000 tomorrow, **without rebuilding**.

### Give it a default in the Dockerfile

```dockerfile
ENV PORT=8000
```

### Change it when you run

```bash
docker run -it -p 3000:3000 -e PORT=3000 ts-node
```

```text
HTTP server running on port 3000
```

| Flag | Meaning |
|---|---|
| `-e PORT=3000` | set one value |
| `-e A=1 -e B=2` | set two values |
| `--env-file ./.env` | read all values from a `.env` file |

```bash
docker run -it -p 8000:8000 --env-file ./.env ts-node
```

### One trap from the lecture

```bash
docker run -p 3000:3000 ts-node        # ❌ app still runs on 8000 inside, nothing answers on 3000
docker run -p 3000:3000 -e PORT=3000 ts-node   # ✅ app now runs on 3000
```

`-p` connects ports. `-e PORT` changes which port the app **uses**. You need both.

---

## Everything together

```dockerfile
FROM node:20.17-alpine
WORKDIR /home/app
COPY package*.json ./
RUN npm install --omit=dev
COPY dist/ ./dist/

RUN addgroup --gid 1001 nodejs
RUN adduser --uid 1001 --ingroup nodejs --disabled-password nodejs
USER nodejs                      # rule 1: not root

ENV PORT=8000                    # rule 3: default setting
EXPOSE 8000                      # rule 2: label the port
CMD ["npm", "start"]
```

(With the multi-stage build from note 232, these lines go in the **last** stage.)

---

## Remember

| Rule | One line |
|---|---|
| **Not root** | `USER nodejs` before `CMD` |
| **Port label** | `EXPOSE 8000` |
| **Settings from outside** | `ENV PORT=8000` in the file, `-e PORT=3000` or `--env-file .env` when running |
| **Secrets** | never write API keys in the Dockerfile. Pass them with `-e` or `--env-file` |

> **If someone asks in an interview:** "Why not run containers as root?" Because a bug in
> the app would give the attacker admin rights inside the container. Create a user with
> `adduser` and switch with `USER` so the app has only the permissions it needs.
