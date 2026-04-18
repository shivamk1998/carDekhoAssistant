import { ChatResponse, Message } from "./types";

const API_URL = "/api";

export async function sendMessage(
  messages: Pick<Message, "role" | "content">[]
): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  return res.json();
}
