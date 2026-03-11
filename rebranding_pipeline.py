import sys
import os
import re
import paramiko
import stat

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ─── CONFIG ───────────────────────────────────────────────────────────────────
HOST = "51.195.109.26"
USER = "ubuntu"
PASSWORD = "BlessdApretadito"

REMOTE_TEMPLATES = "/home/ubuntu/apps/turnosimperio/turnos_app/templates/turnos_app/"
REMOTE_FILES = {
    "/home/ubuntu/apps/turnosimperio/turnos_app/views.py":   "c:/Users/STIVEN ANTEQUERA/Desktop/WEB/turnos-imperio/turnos_app/views.py",
    "/home/ubuntu/apps/turnosimperio/turnos_app/urls.py":    "c:/Users/STIVEN ANTEQUERA/Desktop/WEB/turnos-imperio/turnos_app/urls.py",
    "/home/ubuntu/apps/turnosimperio/turnos_app/models.py":  "c:/Users/STIVEN ANTEQUERA/Desktop/WEB/turnos-imperio/turnos_app/models.py",
    "/home/ubuntu/apps/turnosimperio/turnos_app/forms.py":   "c:/Users/STIVEN ANTEQUERA/Desktop/WEB/turnos-imperio/turnos_app/forms.py",
}
LOCAL_TEMPLATES_DIR = "c:/Users/STIVEN ANTEQUERA/Desktop/WEB/turnos-imperio/turnos_app/templates/turnos_app/"

# ─── SFTP DOWNLOAD ────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Connecting to VPS via SFTP")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=30)
sftp = ssh.open_sftp()
print(f"Connected to {HOST}")

# Download templates directory
print(f"\nDownloading templates from {REMOTE_TEMPLATES}")
downloaded_templates = []
try:
    remote_entries = sftp.listdir_attr(REMOTE_TEMPLATES)
    for entry in remote_entries:
        name = entry.filename
        remote_path = REMOTE_TEMPLATES + name
        local_path = LOCAL_TEMPLATES_DIR + name
        # Only download files (not directories), primarily HTML
        if stat.S_ISREG(entry.st_mode):
            print(f"  Downloading: {name}")
            sftp.get(remote_path, local_path)
            if name.lower().endswith('.html') or name.lower().endswith('.htm'):
                downloaded_templates.append(local_path)
        else:
            print(f"  Skipping dir: {name}")
except Exception as e:
    print(f"  ERROR listing templates dir: {e}")

# Download individual files
print(f"\nDownloading individual Python files...")
for remote_path, local_path in REMOTE_FILES.items():
    try:
        sftp.get(remote_path, local_path)
        print(f"  OK: {os.path.basename(remote_path)}")
    except Exception as e:
        print(f"  ERROR {os.path.basename(remote_path)}: {e}")

sftp.close()
print("\nSFTP download complete.")

# ─── REBRANDING ───────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Applying rebranding to HTML templates")
print("=" * 60)

# Gather all HTML files in local templates dir
all_html = []
for fname in os.listdir(LOCAL_TEMPLATES_DIR):
    if fname.lower().endswith('.html') or fname.lower().endswith('.htm'):
        all_html.append(os.path.join(LOCAL_TEMPLATES_DIR, fname))

print(f"Found {len(all_html)} HTML files to process.")

# ── Text replacements (order matters: most specific first) ──
TEXT_REPLACEMENTS = [
    # Brand name variations
    ("MOTOS TOP",    "IMPERIO MOTOS"),
    ("Motos Top",    "Imperio Motos"),
    ("motos top",    "imperio motos"),
    ("Motostop",     "Imperio Motos"),
    ("motostop",     "imperiomotos"),
    ("MOTOSTOP",     "IMPERIOMOTOS"),
    # URL/domain references
    ("motostop.com.co", "imperiomotos.com.co"),
    ("turnos.motostop", "turnos.imperiomotos"),
]

# ── Logo replacements ──
# Patterns to detect logo references
LOGO_HORIZONTAL = "{% static 'turnos_app/logo-horizontal.png' %}"
LOGO_VERTICAL   = "{% static 'turnos_app/logo-vertical.png' %}"

# Old logo filenames that need replacing
OLD_LOGO_PATTERNS = [
    r"['\"]?(?:{% static ['\"])?turnos_app/(?:img/)?(?:logo\.png|logo2\.png|MOTOS-TOP-VERT\.png|MOTOS-TOP-HORIZ\.png|logo-motostop\.png)['\"]?(?:\s*%\})?['\"]?",
]

# ── Tailwind color class replacements ──
# These are regex-based to handle class= attributes cleanly
# Strategy: replace specific Tailwind classes with inline styles by adding/replacing in the class attribute

# We'll do simple string replacements for color classes within class="..." attributes
# Using a helper that replaces class tokens

COLOR_CLASS_REPLACEMENTS = [
    # Background colors
    ("bg-slate-900",  'style="background-color: #0D0D0D"'),
    ("bg-slate-800",  'style="background-color: #1A1A1A"'),
    ("bg-slate-700",  'style="background-color: #1C1C1C"'),
    ("bg-blue-700",   'style="background-color: #4DC800; color: #000000"'),
    ("bg-blue-600",   'style="background-color: #39FF14; color: #000000"'),
    ("bg-blue-500",   'style="background-color: #39FF14; color: #000000"'),
    # Text colors
    ("text-blue-400", 'style="color: #39FF14"'),
    ("text-blue-300", 'style="color: #4DC800"'),
    ("text-blue-200", 'style="color: #4DC800"'),
    ("text-blue-100", 'style="color: #CCCCCC"'),
    # Border colors
    ("border-blue-500", 'style="border-color: #39FF14"'),
    ("border-blue-600", 'style="border-color: #39FF14"'),
    ("border-slate-600", 'style="border-color: #333333"'),
    ("border-slate-700", 'style="border-color: #222222"'),
]

def apply_text_replacements(content, replacements):
    """Apply simple string replacements, returns (new_content, count)."""
    count = 0
    for old, new in replacements:
        occurrences = content.count(old)
        if occurrences:
            content = content.replace(old, new)
            count += occurrences
    return content, count

def apply_logo_replacements(content):
    """Replace old logo references with new ones based on context."""
    count = 0

    # Pattern 1: {% static 'turnos_app/logo.png' %} style references
    # Detect navbar context: look for nav tags or header context within ~500 chars before
    old_logos = [
        "logo.png", "logo2.png", "MOTOS-TOP-VERT.png",
        "MOTOS-TOP-HORIZ.png", "logo-motostop.png", "MOTOS-TOP-LOGO.png"
    ]

    # Find all img tags with old logos and decide horizontal vs vertical
    def replace_logo_src(match):
        nonlocal count
        full_match = match.group(0)
        src_content = match.group(1)  # content inside src="..."

        # Determine which logo to use based on context
        # Check surrounding context (200 chars before match)
        start = max(0, match.start() - 300)
        context_before = content[start:match.start()].lower()

        # Heuristics: navbar/header → horizontal; main/login/center → vertical
        is_navbar = any(kw in context_before for kw in ['<nav', 'navbar', 'header', 'topbar', 'menu'])
        is_center = any(kw in context_before for kw in ['<main', 'login', 'principal', 'center', 'mx-auto', 'flex-col'])

        if is_navbar:
            new_src = LOGO_HORIZONTAL
        else:
            new_src = LOGO_VERTICAL

        count += 1
        return full_match.replace(src_content, new_src)

    # Match src="..." or src='...' containing old logo names
    old_logo_pattern = '|'.join(re.escape(l) for l in old_logos)
    # Match: src="{% static 'turnos_app/logo.png' %}" or src="/static/turnos_app/logo.png"
    pattern = re.compile(
        r'src=["\']([^"\']*(?:' + old_logo_pattern + r')[^"\']*)["\']',
        re.IGNORECASE
    )
    new_content = pattern.sub(replace_logo_src, content)

    # Also handle bare references like: url 'logo.png' outside of src attributes
    # e.g. background-image: url(...)
    def replace_bg_logo(match):
        nonlocal count
        count += 1
        return match.group(0).replace(match.group(1), LOGO_HORIZONTAL)

    bg_pattern = re.compile(
        r'url\(["\']?([^)"\']*(?:' + old_logo_pattern + r')[^)"\']*)["\']?\)',
        re.IGNORECASE
    )
    new_content = bg_pattern.sub(replace_bg_logo, new_content)

    return new_content, count

def apply_color_class_replacements(content, replacements):
    """
    Replace Tailwind color classes in class="..." attributes.
    When a class token is found inside class="", replace the whole class attr token
    with an equivalent inline style, and remove the old class token.
    """
    count = 0

    for old_class, new_style in replacements:
        # Match class="... old_class ..." patterns
        # We need to remove the old_class from class="" and add the style attribute

        # Pattern: find elements with class attributes containing old_class
        # Strategy: replace the class token within class="..." with nothing,
        # and append the style="" to the tag opening

        # Simpler approach: replace standalone class token in class="..."
        # by removing it from class attr and noting it needs a style

        # We'll use a two-pass: first mark occurrences, then process
        # Actually, simplest robust approach for templates: just do word-boundary replacement
        # of the class name inside class attributes

        # Find all class="..." or class='...' attributes
        def replace_in_class_attr(m):
            nonlocal count
            classes = m.group(1)
            # Check if old_class is present as a whole word
            new_classes = re.sub(r'\b' + re.escape(old_class) + r'\b', '', classes)
            if new_classes != classes:
                count += 1
                return 'class="' + new_classes.strip() + '"'
            return m.group(0)

        content = re.sub(r'class="([^"]*)"', replace_in_class_attr, content)

        # For single-quoted class attributes
        def replace_in_class_attr_sq(m):
            nonlocal count
            classes = m.group(1)
            new_classes = re.sub(r'\b' + re.escape(old_class) + r'\b', '', classes)
            if new_classes != classes:
                count += 1
                return "class='" + new_classes.strip() + "'"
            return m.group(0)

        content = re.sub(r"class='([^']*)'", replace_in_class_attr_sq, content)

    return content, count

def add_body_background(content):
    """Ensure body tag has black background."""
    count = 0
    # If body tag doesn't have a background style, add one
    def add_bg_to_body(m):
        nonlocal count
        tag = m.group(0)
        if 'background' not in tag and 'style=' not in tag:
            count += 1
            return tag.rstrip('>') + ' style="background-color: #000000; color: #FFFFFF">'
        elif 'style=' in tag and 'background' not in tag:
            count += 1
            return re.sub(r'style="([^"]*)"', r'style="background-color: #000000; color: #FFFFFF; \1"', tag)
        return tag
    content = re.sub(r'<body[^>]*>', add_bg_to_body, content, flags=re.IGNORECASE)
    return content, count

# ── Process each HTML file ──
total_stats = {
    'files_modified': 0,
    'text_replacements': 0,
    'logo_replacements': 0,
    'color_replacements': 0,
}

file_reports = []

for fpath in sorted(all_html):
    fname = os.path.basename(fpath)
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            original = f.read()
    except Exception as e:
        print(f"  ERROR reading {fname}: {e}")
        continue

    content = original
    file_changes = {}

    # 1. Text replacements
    content, n = apply_text_replacements(content, TEXT_REPLACEMENTS)
    file_changes['text'] = n
    total_stats['text_replacements'] += n

    # 2. Logo replacements
    content, n = apply_logo_replacements(content)
    file_changes['logos'] = n
    total_stats['logo_replacements'] += n

    # 3. Color class removals (from class attrs)
    content, n = apply_color_class_replacements(content, COLOR_CLASS_REPLACEMENTS)
    file_changes['colors'] = n
    total_stats['color_replacements'] += n

    # 4. Body background
    content, n = add_body_background(content)
    file_changes['body_bg'] = n

    # 5. Title tag cleanup
    def fix_title(m):
        title_content = m.group(1)
        # Apply text replacements to title
        for old, new in TEXT_REPLACEMENTS:
            title_content = title_content.replace(old, new)
        # If no brand name at all, ensure Imperio Motos is there
        if 'Imperio Motos' not in title_content and 'IMPERIO MOTOS' not in title_content:
            title_content = 'Imperio Motos | ' + title_content.strip()
        return f'<title>{title_content}</title>'
    content = re.sub(r'<title>(.*?)</title>', fix_title, content, flags=re.IGNORECASE | re.DOTALL)

    if content != original:
        total_stats['files_modified'] += 1
        try:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            status = "MODIFIED"
        except Exception as e:
            status = f"WRITE ERROR: {e}"
    else:
        status = "unchanged"

    report = f"  {status:12s} {fname:40s} text={file_changes['text']} logos={file_changes['logos']} colors={file_changes['colors']}"
    print(report)
    file_reports.append(report)

print(f"\nRebranding summary:")
print(f"  Files modified   : {total_stats['files_modified']}")
print(f"  Text replacements: {total_stats['text_replacements']}")
print(f"  Logo replacements: {total_stats['logo_replacements']}")
print(f"  Color removals   : {total_stats['color_replacements']}")

# ─── GIT COMMIT & PUSH ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Git commit and push")
print("=" * 60)

import subprocess

REPO_DIR = "c:/Users/STIVEN ANTEQUERA/Desktop/WEB/turnos-imperio"

def run_git(args, cwd=REPO_DIR):
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

# git add
code, out, err = run_git(["add", "."])
print(f"git add: {'OK' if code == 0 else 'FAIL'}")
if err: print(f"  {err}")

# git status
code, out, err = run_git(["status", "--short"])
print(f"Staged files:\n{out}")

# git commit
commit_msg = "Rebranding completo: Motos Top \u2192 Imperio Motos (logos, colores, textos)"
code, out, err = run_git(["commit", "-m", commit_msg])
print(f"git commit: {'OK' if code == 0 else 'FAIL'}")
print(f"  {out}")
if err and code != 0:
    print(f"  STDERR: {err}")

# git push
code, out, err = run_git(["push", "origin", "main"])
print(f"git push: {'OK' if code == 0 else 'FAIL'}")
print(f"  {out}")
if err:
    print(f"  {err}")

push_ok = (code == 0)

# ─── VPS DEPLOY ───────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Deploy on VPS (git pull + restart service)")
print("=" * 60)

ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect(HOST, username=USER, password=PASSWORD, timeout=30)

commands = [
    "cd /home/ubuntu/apps/turnosimperio && git pull origin main",
    "sudo systemctl restart turnosimperio",
    "sudo systemctl status turnosimperio --no-pager -l | head -20",
]

for cmd in commands:
    print(f"\n$ {cmd}")
    stdin, stdout, stderr = ssh2.exec_command(cmd, timeout=60)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out)
    if err:
        print(f"STDERR: {err}")

ssh2.close()

# ─── FINAL REPORT ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FINAL REPORT")
print("=" * 60)
print(f"Files modified   : {total_stats['files_modified']}")
print(f"Text replacements: {total_stats['text_replacements']}")
print(f"Logo replacements: {total_stats['logo_replacements']}")
print(f"Color removals   : {total_stats['color_replacements']}")
print(f"Git push         : {'SUCCESS' if push_ok else 'FAILED'}")
print("Done.")
