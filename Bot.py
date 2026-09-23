import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ["8875846282:AAHphZaeFkrI9l6pYF9kveId-_JWMOSDrxY"]
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "@Movielokadmin")

USDT_BEP20 = os.environ.get("USDT_BEP20", "0xd919b57e36dfa8b3512a17adad75Dc6174EeDa87")
USDT_TRC20 = os.environ.get("USDT_TRC20", "TBY9a994oJQkPkj1KsR8WX5FFKNfF9ntLc")
BTC_ADDRESS = os.environ.get("BTC_ADDRESS", "bc1q7xg7gjp94vpe49m4mv856tctt68re8nlju9hl8")

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "@Movielokadmin"
)


# =========================
# MAIN MENU
# =========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💎 Membership", callback_data="membership")],
        [InlineKeyboardButton("🆕 New Release", callback_data="new_release")],
        [InlineKeyboardButton("👥 Referral", callback_data="referral")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# MEMBERSHIP MENU
# =========================

def membership_menu():
    keyboard = [
        [InlineKeyboardButton("🆓 Free", callback_data="free")],
        [InlineKeyboardButton("💳 Paid", callback_data="paid")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ]

    return InlineKeyboardMarkup(keyboard)


def paid_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Weekly Access — $3.99",
                              callback_data="weekly")],
        [InlineKeyboardButton("📅 Annual Access — $49.99",
                              callback_data="annual")],
        [InlineKeyboardButton("⭐ Special Access — $199.99",
                              callback_data="special")],
        [InlineKeyboardButton("🔙 Back", callback_data="membership")],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# PAYMENT MENU
# =========================

def payment_menu(plan):
    keyboard = [
        [
            InlineKeyboardButton(
                "USDT",
                callback_data=f"usdt_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "BTC",
                callback_data=f"btc_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="paid"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def usdt_menu(plan):
    keyboard = [
        [
            InlineKeyboardButton(
                "USDT BEP-20",
                callback_data=f"bep20_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "USDT TRC-20",
                callback_data=f"trc20_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data=f"payment_{plan}"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🎬 <b>Welcome to Movie Bot</b>\n\n"
        "Choose an option from the menu below."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ---------------------
    # MAIN MENU
    # ---------------------

    if data == "back_main":

        await query.edit_message_text(
            "🎬 <b>Main Menu</b>",
            parse_mode="HTML",
            reply_markup=main_menu()
        )

    # ---------------------
    # MEMBERSHIP
    # ---------------------

    elif data == "membership":

        await query.edit_message_text(
            "💎 <b>Membership</b>\n\n"
            "Choose your membership option:",
            parse_mode="HTML",
            reply_markup=membership_menu()
        )

    # ---------------------
    # FREE MEMBERSHIP
    # ---------------------

    elif data == "free":

        text = (
            "🆓 <b>Free Membership</b>\n\n"
            "To become eligible for free access, "
            "complete the referral requirements.\n\n"
            "Your referral progress will be shown here "
            "once the referral system is connected."
        )

        keyboard = [
            [InlineKeyboardButton(
                "👥 My Referral",
                callback_data="referral"
            )],
            [InlineKeyboardButton(
                "🔙 Back",
                callback_data="membership"
            )],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # PAID
    # ---------------------

    elif data == "paid":

        await query.edit_message_text(
            "💳 <b>Paid Membership</b>\n\n"
            "Choose an access period:",
            parse_mode="HTML",
            reply_markup=paid_menu()
        )

    # ---------------------
    # PLANS
    # ---------------------

    elif data in ["weekly", "annual", "special"]:

        names = {
            "weekly": "Weekly Access — $3.99",
            "annual": "Annual Access — $49.99",
            "special": "Special Access — $199.99",
        }

        await query.edit_message_text(
            f"💳 <b>{names[data]}</b>\n\n"
            "Choose your payment method:",
            parse_mode="HTML",
            reply_markup=payment_menu(data)
        )

    # ---------------------
    # PAYMENT
    # ---------------------

    elif data.startswith("payment_"):

        plan = data.replace("payment_", "")

        await query.edit_message_text(
            "💰 <b>Select Payment Method</b>",
            parse_mode="HTML",
            reply_markup=payment_menu(plan)
        )

    # ---------------------
    # USDT
    # ---------------------

    elif data.startswith("usdt_"):

        plan = data.replace("usdt_", "")

        await query.edit_message_text(
            "💵 <b>USDT Payment</b>\n\n"
            "Choose the network:",
            parse_mode="HTML",
            reply_markup=usdt_menu(plan)
        )

    # ---------------------
    # BEP20
    # ---------------------

    elif data.startswith("bep20_"):

        plan = data.replace("bep20_", "")

        text = (
            "💵 <b>USDT BEP-20</b>\n\n"
            f"<code>{USDT_BEP20}</code>\n\n"
            "⚠️ Send USDT only through the BEP-20 network.\n\n"
            "After completing the payment, press "
            "<b>Payment Done ✅</b>."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Payment Done",
                    callback_data=f"paid_done_{plan}_bep20"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data=f"usdt_{plan}"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # TRC20
    # ---------------------

    elif data.startswith("trc20_"):

        plan = data.replace("trc20_", "")

        text = (
            "💵 <b>USDT TRC-20</b>\n\n"
            f"<code>{USDT_TRC20}</code>\n\n"
            "⚠️ Send USDT only through the TRC-20 network.\n\n"
            "After completing the payment, press "
            "<b>Payment Done ✅</b>."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Payment Done",
