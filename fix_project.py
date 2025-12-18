import os
folder = os.getcwd()
print(f"🔧 Scanning for HTML files in: {folder}")
for filename in os.listdir(folder):
    if filename.endswith(".html"):
        filepath = os.path.join(folder, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if '<base href="/">' not in content and "<head>" in content:
            content = content.replace("<head>", '<head>\n    <base href="/">')
            print(f"   -> Added <base> tag to {filename}")

        if 'href="style.css"' in content:
            content = content.replace('href="style.css"', 'href="/style.css"')
            print(f"   -> Fixed CSS link in {filename}")
        if 'src="script.js"' in content:
            content = content.replace('src="script.js"', 'src="/script.js"')
            print(f"   -> Fixed JS link in {filename}")

        # Save changes
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


print("\n✅ All HTML files have been fixed! You can now run 'python app.py'")
