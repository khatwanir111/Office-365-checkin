import random
import datetime

def get_m365_dev_quote():
    quotes = [
        "Empower your users—build smarter apps with Microsoft Graph.",
        "Good code is clean. Great code is collaborative. – A Microsoft 365 Dev",
        "APIs are your superpower. Use Microsoft Graph to connect the dots.",
        "Build once, integrate everywhere—Microsoft Teams is your dev playground.",
        "Keep your code DRY and your identity secure—Azure AD is your friend.",
        "Great apps don’t just work—they work with Microsoft 365."
    ]
    return random.choice(quotes)

def get_today_focus_area():
    focus_areas = [
        "Extend Microsoft Teams with custom tabs and bots",
        "Explore Microsoft Graph API for calendar insights",
        "Integrate Outlook with actionable messages",
        "Develop SPFx web parts for SharePoint Online",
        "Implement SSO with Azure AD for your app",
        "Automate workflows using Power Automate SDK"
    ]
    return random.choice(focus_areas)

def main():
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    print(f"🔧 Microsoft 365 Dev Log – {today}")
    print("="*60)
    print(f"🧠 Dev Quote of the Day:\n\"{get_m365_dev_quote()}\"\n")
    print(f"🎯 Today's Focus Area:\n{get_today_focus_area()}\n")
    print("💡 Tip: Visit https://learn.microsoft.com/microsoft-365/dev for docs & samples!")

if __name__ == "__main__":
    main()
