import ReactMarkdown from "react-markdown";
import { Message } from "../types";
import { Bot, User } from "lucide-react";
import CarCard from "./CarCard";
import ComparisonTable from "./ComparisonTable";

interface Props {
  message: Message;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? "bg-blue-600" : "bg-gray-200"
        }`}
      >
        {isUser ? (
          <User size={16} className="text-white" />
        ) : (
          <Bot size={16} className="text-gray-600" />
        )}
      </div>

      {/* Content */}
      <div className={`max-w-[80%] ${isUser ? "text-right" : ""}`}>
        <div
          className={`inline-block rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
            isUser
              ? "bg-blue-600 text-white rounded-tr-md"
              : "bg-white border border-gray-200 text-gray-800 rounded-tl-md shadow-sm"
          }`}
        >
          <div className={isUser ? "" : "chat-markdown"}>
            {isUser ? (
              message.content
            ) : (
              <ReactMarkdown>{message.content}</ReactMarkdown>
            )}
          </div>
        </div>

        {/* Car Cards */}
        {message.cars && message.cars.length > 0 && (
          <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {message.cars.map((car) => (
              <CarCard key={car.id} car={car} />
            ))}
          </div>
        )}

        {/* Comparison Table */}
        {message.comparison && (
          <div className="mt-3 bg-white border border-gray-200 rounded-xl p-3 shadow-sm overflow-hidden">
            <ComparisonTable comparison={message.comparison} />
          </div>
        )}
      </div>
    </div>
  );
}
