import json

def process_chat_log(chat_file):
    structured_chat = {
        "conversation_id": "chat_001",
        "messages": []
    }

    with open(chat_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if line.startswith("Customer:"):
            role = "customer"
            content = line.replace("Customer:", "").strip()

        elif line.startswith("Agent:"):
            role = "agent"
            content = line.replace("Agent:", "").strip()

        else:
            continue

        structured_chat["messages"].append({
            "role": role,
            "content": content
        })

    return structured_chat


if __name__ == "__main__":
    # IMPORTANT: Correct path from root folder
    result = process_chat_log("sample_data/chats/chat_1.txt")

    print("\n===== STRUCTURED CHAT OUTPUT =====\n")
    print(json.dumps(result, indent=2))
