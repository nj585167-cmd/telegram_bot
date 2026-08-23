import os
from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from langchain_core.messages import HumanMessage

from ai_agent import agent

TOKEN = os.getenv("tel_key")


def extract_text(msg):
    """Gemini sometimes returns a list of blocks instead of a string."""
    c = msg.content
    if isinstance(c, str):
        return c
    parts = [b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"]
    return "\n".join(p for p in parts if p).strip() or "(no reply)"


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=update.message.text)]},
        config={"configurable": {"thread_id": str(update.effective_chat.id)}},
    )
    await update.message.reply_text(extract_text(result["messages"][-1]))


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))


if os.getenv("RENDER_EXTERNAL_URL"):
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ["PORT"]),
        url_path=TOKEN,
        webhook_url=f"{os.environ['RENDER_EXTERNAL_URL']}/{TOKEN}",
    )
else:
    print("polling locally")
    app.run_polling()