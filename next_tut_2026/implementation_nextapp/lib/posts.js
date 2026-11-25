// Fake "database". In a real app this would be a DB or API call.
const posts = [
  { id: "1", title: "What is Next.js?", body: "A React framework for routing, rendering and APIs." },
  { id: "2", title: "Folders are routes", body: "The folder structure inside app/ becomes the URL." },
  { id: "3", title: "Layouts stay mounted", body: "A layout keeps its state while you move between pages." },
];

export function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function getPosts() {
  return posts;
}

export async function getPost(id) {
  return posts.find((post) => post.id === id) ?? null;
}
