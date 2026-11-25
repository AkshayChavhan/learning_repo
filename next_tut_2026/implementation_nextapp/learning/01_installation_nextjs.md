# 01: Installation

> Notes: [01_nextjs.md](../../notes/01_nextjs.md) — "What is Next.js?"

## Concept

**Next.js** is a React framework: routing, server rendering, data fetching and API routes on top of React. It runs on **Node.js**.

## What was done

Scaffolded the app with `create-next-app` (Next.js **16.4.6**, React 19.3.0):

```bash
npx create-next-app@16.4.6 . --js --app --no-tailwind --no-eslint --no-src-dir \
  --import-alias "@/*" --use-npm --disable-git --yes
```

| Option | Why |
|---|---|
| `--app` | Use the App Router (`app/` folder), the current default |
| `--js` | Plain JavaScript, same as the notes' examples |
| `--no-src-dir` | Keep `app/` at the project root, as in the notes |
| `--import-alias "@/*"` | Lets us write `@/lib/posts` instead of `../../lib/posts` |

Generated files that matter:

| File | Purpose |
|---|---|
| `package.json` | Scripts: `dev`, `build`, `start` |
| `next.config.mjs` | Config. The generated file enables `cacheComponents: true` (see gotchas) |
| `jsconfig.json` | Defines the `@/*` alias |
| `AGENTS.md` | Auto-generated note telling tools to read the bundled docs in `node_modules/next/dist/docs/` |

## See it working

```bash
npm run dev
```

Open `http://localhost:3000`. You should see the "Mini Blog" header and the Home page.

Production check:

```bash
npm run build
```

```text
Route (app)
┌ ○ /
├ ○ /about
├ ◐ /posts
...
○ (Static)   ◐ (Partial Prerender)   ƒ (Dynamic)
```

## Gotchas

- **Use Node 20.9+** (this machine: Node 24.22.1, npm 11.19.1).
- **Empty folders block scaffolding.** `create-next-app` refused to run in a folder that had empty `app/`, `public/` folders. Remove them first.
- **Lockfile warning.** This project sits inside a parent git repo, so `next build` prints *"ignored package-lock.json … outside the current Git repository"*. It is harmless. Fix by setting `turbopack.root` in `next.config.mjs` if you want it gone.
- **Next 16 ships its own docs.** `AGENTS.md` points to `node_modules/next/dist/docs/`. Check there when a notes example does not work.
