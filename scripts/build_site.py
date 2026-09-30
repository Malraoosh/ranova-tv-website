"""Generates the Ranova TV website pages. Run: python scripts/build_site.py --email you@example.com [--release-ready]"""
from pathlib import Path
import argparse, html, re

SITE = Path(__file__).resolve().parents[1]
UPDATED = '30 September 2026'
parser = argparse.ArgumentParser(description='Generate the Ranova TV static website.')
parser.add_argument('--email', default='')
parser.add_argument('--release-ready', action='store_true', help='Use only after reviewing the policy and testing deletion behavior.')
args = parser.parse_args()
if args.email and not re.fullmatch(r'[A-Za-z0-9.!#$%&\'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', args.email):
    parser.error('Enter a valid support email address.')
if args.release_ready and not args.email:
    parser.error('--release-ready requires --email.')
email = html.escape(args.email, quote=True)
contact = f'<a class="email" href="mailto:{email}">{email}</a>' if email else '<p class="muted">Our public support email will be added before the app launches.</p>'
draft = '' if args.release_ready else '<p class="panel small" role="note"><strong>Pre-release preview.</strong> These pages are being prepared for launch. The public support contact and final policy review are still pending.</p>'
nav_items = [('index.html', 'Home'), ('support.html', 'Support'), ('privacy.html', 'Privacy'), ('terms.html', 'Terms')]


def document(filename, title, description, body):
    nav = ''.join(f'<a href="{url}"' + (' aria-current="page"' if url == filename else '') + f'>{label}</a>' for url, label in nav_items)
    robots = '' if args.release_ready else '<meta name="robots" content="noindex, nofollow">'
    t, d = html.escape(title, quote=True), html.escape(description, quote=True)
    (SITE / filename).write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t} | Ranova TV</title><meta name="description" content="{d}">{robots}
<meta name="theme-color" content="#0b0c18"><meta property="og:title" content="{t} | Ranova TV"><meta property="og:description" content="{d}"><meta property="og:type" content="website"><meta property="og:image" content="assets/ranova-mark-512.png">
<link rel="icon" href="assets/favicon-32.png" type="image/png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/unbounded-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><div class="wrap">
<header class="header"><a class="brand" href="index.html"><img src="assets/ranova-mark-96.png" alt="" width="38" height="38">Ranova TV</a><nav class="nav" aria-label="Main">{nav}</nav></header>
<main id="main">{body}</main>
<footer class="footer"><span>© 2026 Ranova TV. A TV player for media sources you already have.</span><nav aria-label="Footer"><a href="support.html">Support</a><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a></nav></footer>
</div></body></html>
''', encoding='utf-8')


TILES = [('live', 'Live TV'), ('movies', 'Movies'), ('series', 'Series'), ('mylist', 'My List')]
tv = f'''<figure class="tv"><div class="tv-frame"><div class="tv-screen">
<img src="assets/app/welcome.webp" alt="" width="1672" height="941" fetchpriority="high">
<div class="tv-ui" aria-hidden="true">
<div class="tv-bar"><img src="assets/ranova-mark-96.png" alt=""><b>Ranova TV</b><span class="on">Home</span><span>Live TV</span><span>Movies</span><span>Series</span><span>My List</span><span>Search</span><span>Settings</span><span class="clock">21:16</span></div>
<div class="tv-hero"><small>Welcome to</small><strong>Ranova TV</strong><span>Discover a world of live TV, movies and series all in one place.</span></div>
<div class="tv-rail"><i class="tv-focus"></i>{''.join(f'<div class="tv-tile"><img src="assets/app/tile-{k}.webp" alt="" loading="lazy"><span>{v}</span></div>' for k, v in TILES)}</div>
</div></div></div>
<figcaption>The Ranova TV home screen, driven entirely by your TV remote.</figcaption></figure>'''

document('index.html', 'A TV player for your own sources', 'Ranova TV is a media player for Samsung, LG, and Android TV. Connect your own M3U playlist or Xtream login to watch live TV, movies, and series.', f'''
<section class="intro"><h1>Bring your playlist. Ranova TV does the rest on the big screen.</h1>
<p class="lead">A player for Samsung, LG, and Android TV. Add your own M3U playlist or Xtream login and watch live TV, movies, and series with a proper guide.</p>
<div class="actions"><a class="button" href="support.html">Get help</a><a class="button quiet" href="privacy.html">How your data is handled</a></div>
<p class="note">Launching soon. Store links will appear here once each store approves the app.</p></section>
{tv}
<div class="platforms"><span>Coming to</span><strong>Samsung Smart TV</strong><strong>LG webOS</strong><strong>Android TV and Google TV</strong></div>
<section class="block"><h2>Ready in three steps</h2><p class="muted">Everything is set up on the TV with your remote. No account, no website sign-up.</p>
<ol class="steps"><li><h3>Add your source</h3><p>Enter an M3U playlist URL, with an optional XMLTV guide, or your Xtream server and login.</p></li>
<li><h3>Let it load</h3><p>Ranova TV reads your channels, movies, series, and programme guide, then refreshes them on the schedule you choose.</p></li>
<li><h3>Press play</h3><p>Browse by category, zap by channel number, or search across every source you have added.</p></li></ol></section>
<section class="block"><h2>Made for a remote, not a mouse</h2>
<dl class="features"><div><dt>Live TV with a full guide</dt><dd>See what is on now and next, and jump straight to a channel by number.</dd></div>
<div><dt>Movies and series</dt><dd>Browse on-demand titles from Xtream sources, with details and trailers where your provider lists them.</dd></div>
<div><dt>My List and Continue watching</dt><dd>Save channels, movies, and series for later, and resume a title from where you stopped.</dd></div>
<div><dt>Search every source</dt><dd>One search covers the channels and titles of all your sources.</dd></div>
<div><dt>More than one source</dt><dd>Add several playlists or logins and switch between them.</dd></div>
<div><dt>English and Arabic</dt><dd>Full right-to-left layout when you switch to Arabic.</dd></div></dl></section>
<section class="disclosure"><h2>Ranova TV doesn’t come with channels.</h2>
<div><p>It is a player. It includes no channels, movies, playlists, or IPTV subscriptions, and it isn’t affiliated with any provider. You bring a source you have permission to use, and you are responsible for the content you access through it.</p></div></section>''')

document('support.html', 'Help and support', 'Get help with Ranova TV: contact support, fix connection and playback problems, and manage your data.', f'''
<div class="page-head"><h1>Help and support</h1><p class="lead">Answers to common questions, and how to reach us when something isn’t working.</p></div>{draft}
<div class="support"><section class="panel contact"><h2>Email support</h2><p class="muted">Write to us about problems with the app, privacy questions, or a copyright concern about this app or website.</p>{contact}<p class="small">Never send your provider password, payment details, or a playlist URL that contains your login.</p></section>
<section class="panel"><h2>Include these details</h2><ul><li>Your TV brand, model, and operating system</li><li>The Ranova TV version, from your TV’s app information or store page</li><li>What happened, and the steps that lead to it</li><li>Any error message, or a screenshot with personal details hidden</li></ul></section></div>
<section class="faq"><h2>Common questions</h2>
<details><summary>Does Ranova TV include channels or an IPTV subscription?</summary><p>No. Ranova TV is a player. You need your own compatible source and permission to access the content it provides.</p></details>
<details><summary>My source won’t connect. What should I check?</summary><p>Check your internet connection, then check the server address and login details with your provider, and make sure your subscription is active. For account access, connection limits, or expired logins, contact your provider.</p></details>
<details><summary>A stream buffers or won’t play. What can I try?</summary><p>Try another channel or title, check your TV’s network connection, and restart the app. A wired connection often helps when Wi-Fi is weak. Playback also depends on the provider’s server and on whether your TV supports the stream’s format.</p></details>
<details><summary>Where are my logins and watch history stored?</summary><p>On your TV only. The app still talks to your provider to sign in and play media. The <a href="privacy.html">Privacy Policy</a> explains this in full.</p></details>
<details><summary>How do I remove my data?</summary><p>To remove one source, open Settings, then Sources, and choose Delete. This removes its login, channels, guide, My List items, and resume positions. To remove everything, uninstall the app or clear its data in your TV’s settings. Contact your provider separately about information your provider holds.</p></details>
<details><summary>Where can I download Ranova TV?</summary><p>The app is being prepared for Samsung Smart TV, LG webOS, and Android TV / Google TV. Store links will be added to this website when it is available.</p></details>
</section>''')


def legal(filename, title, intro, sections):
    toc = ''.join(f'<a href="#{slug}">{name}</a>' for slug, name, _ in sections)
    content = ''.join(f'<section id="{slug}"><h2>{name}</h2>{body}</section>' for slug, name, body in sections)
    stamp = ('Last updated ' if args.release_ready else 'Draft prepared ') + UPDATED
    document(filename, title, f'{title} for the Ranova TV media player and its website.',
             f'<div class="page-head"><h1>{title}</h1><p class="lead">{intro}</p><p class="meta">{stamp}</p></div>{draft}'
             f'<div class="legal"><nav class="toc" aria-label="On this page"><b>On this page</b>{toc}</nav><div class="prose">{content}</div></div>')


# Every statement below was checked against the app code (D:/WorkSpace/RanovaTV, v0.2.0). Re-check when the app changes.
legal('privacy.html', 'Privacy Policy', 'What Ranova TV stores on your TV, who it talks to, and how to remove your information.', [
    ('scope', 'Who this covers', '<p>This policy covers the Ranova TV app for Samsung Smart TV, LG webOS, and Android TV / Google TV, and this website. Ranova TV is made by Mohammad Al Raoosh, an independent developer based in Jordan. The providers you connect are independent services with their own privacy policies.</p>'),
    ('summary', 'In short', '<ul><li>There is no Ranova TV account and no Ranova TV server. What you enter is stored on your TV and shared only with the provider it belongs to.</li><li>The app has no advertising, analytics, or crash-reporting tools.</li><li>To work, the app connects to your provider, and in two cases to other services, described below.</li></ul>'),
    ('stored', 'What is stored on your TV', '<p>The app keeps the following in its own storage on your TV:</p><ul><li><strong>Your sources:</strong> the name you give each one, its playlist or server address, guide address, and the username and password you enter.</li><li><strong>Your provider’s catalogue:</strong> the channels, movies, series, and programme guide downloaded from your sources, so the app can open quickly.</li><li><strong>My List</strong> and <strong>resume positions</strong>, which power Continue watching.</li><li><strong>Settings</strong> such as language, theme, playback buffer, and which source you used last.</li></ul><p>None of this is sent to the developer. The app does not keep a record of your searches.</p><p>Your login details are kept in the app’s private storage but are not encrypted there. Anyone with access to your TV’s app data could read them, so keep your TV secured.</p>'),
    ('device', 'Device ID', '<p>The app reads your TV’s device identifier, which your TV’s platform provides, and shows it in Settings under About. It is used only on your TV and is not sent anywhere.</p>'),
    ('providers', 'Connections to your provider', '<p>When you add a source, the app connects to that provider to sign in, download listings and the guide, load artwork, and play streams. Your provider receives your login details, your requests, and your TV’s IP address, as with any app that uses its service.</p><p>Some providers use plain HTTP rather than HTTPS. Over HTTP, your login details and viewing requests are not encrypted in transit. With Xtream sources, your username and password are part of the request address. Use HTTPS addresses where your provider offers them.</p>'),
    ('third-parties', 'Other services the app contacts', '<ul><li><strong>Lorem Picsum</strong> (picsum.photos): the home screen downloads decorative background photos from this image service. This request shares your TV’s IP address with it. It does not include anything about you or your sources.</li><li><strong>YouTube</strong>: when you open a movie or series whose provider lists a trailer, the app asks YouTube whether that trailer exists. This shares your IP address and the trailer’s video ID with Google. If you choose Trailer, the YouTube app opens and Google’s privacy policy applies there.</li></ul><p>The app uses no other outside services. It downloads no fonts from the internet and uses no tracking or advertising services.</p>'),
    ('backup', 'Backups', '<p>On Android TV, the app’s data is excluded from Google cloud backup and device-to-device transfer. Ranova TV makes no backups of its own on any platform.</p>'),
    ('removal', 'Removing your information', '<ul><li><strong>Remove one source:</strong> in Settings, open Sources and choose Delete, or open the source and choose Remove source. This deletes its login, channels, guide, My List items, and resume positions from your TV.</li><li><strong>Remove everything:</strong> uninstall Ranova TV, or clear its data from your TV’s app settings.</li><li><strong>Remove one item from My List:</strong> open the title and select In My List.</li></ul><p>The developer has no access to anything stored on your TV, so it cannot be deleted remotely. Removing a source does not delete what your provider holds about you. For that, contact your provider.</p>'),
    ('support', 'When you contact support', '<p>If you email support, we receive your email address, your message, and any attachments. We use them only to answer you. The email is handled by our email service provider and kept only as long as needed to resolve your request. Please don’t send passwords, payment details, or playlist addresses that contain your login. You can ask us to delete your emails at any time.</p>'),
    ('rights', 'Your rights', '<p>Depending on where you live, you may have the right to access, correct, or delete personal information we hold. In practice this is only support email, because the app sends us nothing. To make a request, contact us using the details below.</p>'),
    ('children', 'Children', '<p>Ranova TV is not directed at children, and we do not knowingly collect information from children.</p>'),
    ('website', 'This website', '<p>This website has no advertising, analytics, cookies, forms, or scripts, and its fonts and images are served with the site. It is hosted on GitHub Pages, and GitHub logs visitors’ IP addresses for security, as described in the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy Statement</a>.</p>'),
    ('changes', 'Changes to this policy', '<p>We will update this page before the app’s data practices change, for example if we add accounts, pairing with a phone, sync, analytics, or payments. The date at the top shows the current version.</p>'),
    ('contact', 'Contact', f'<p><strong>Mohammad Al Raoosh</strong>, developer of Ranova TV, Jordan.</p>{contact}'),
])

legal('terms.html', 'Terms of Service', 'The terms for using Ranova TV with your own media sources.', [
    ('player', 'What Ranova TV is', '<p>Ranova TV is a media player made by Mohammad Al Raoosh. It plays content from sources you add. It doesn’t supply or sell channels, movies, playlists, IPTV subscriptions, or logins. These terms cover the app and this website.</p>'),
    ('sources', 'Your sources and permissions', '<p>You are responsible for getting your own source and for having permission to access its content. Use the app lawfully and follow your provider’s terms. Don’t use Ranova TV to infringe copyright, get around access restrictions, or use a service without authorization.</p><p>Ranova TV does not endorse, check, or control the services you connect. Your agreement with a provider is separate from these terms.</p>'),
    ('use', 'Using the app', '<p>You may use a lawfully obtained copy of Ranova TV to play media. Don’t misuse the app or website, interfere with how they work, or distribute modified copies as official Ranova TV software. These terms don’t restrict anything applicable law allows you to do.</p>'),
    ('compatibility', 'Availability and playback', '<p>Playback depends on your TV, your network, your provider, your account, and the media format. A stream or feature may not work on every TV or with every source. We may update the app or change what it supports.</p><p>We can’t guarantee uninterrupted access to third-party content. For missing titles, expired subscriptions, or account problems, contact your provider.</p>'),
    ('trailers', 'Trailers', '<p>Trailers open in the YouTube app, which has its own terms from Google.</p>'),
    ('payments', 'Payments', '<p>Ranova TV is currently free. Payments to your provider are governed by that provider’s terms and refund policy, and we can’t manage or refund them.</p><p>If paid features are added later, their price and billing terms will be shown before you buy. You are never required to buy them.</p>'),
    ('privacy', 'Privacy', '<p>The <a href="privacy.html">Privacy Policy</a> explains what the app stores on your TV, which services it contacts, and how to remove your information.</p>'),
    ('rights', 'Ownership and copyright', '<p>The Ranova TV software and brand belong to the developer. Content you access through a source belongs to its rights holders, and connecting a source gives you no extra rights to it.</p><p>To report a copyright concern about the app or this website, email us from the <a href="support.html">support page</a> and describe the material and the rights involved. For content supplied by a provider, contact that provider.</p>'),
    ('limitations', 'Limitations and consumer rights', '<p>To the extent the law allows, the app is provided as it is, without a promise that it will be free of errors or work with every source. We are not responsible for a provider’s content, availability, security, or account decisions.</p><p>Nothing in these terms removes consumer rights or liability that cannot legally be excluded. Where these terms conflict with those rights, your rights under the law win.</p>'),
    ('updates', 'Changes and contact', f'<p>We may update these terms as the app changes. The date at the top shows the current version. For questions, contact <strong>Mohammad Al Raoosh</strong>, developer of Ranova TV, Jordan.</p>{contact}'),
])

document('404.html', 'Page not found', 'The page you requested could not be found.', '<section class="page-head lost"><h1>This page isn’t here.</h1><p class="lead">It may have moved, or the address may be incomplete.</p><div class="actions"><a class="button" href="index.html">Go to the home page</a><a class="button quiet" href="support.html">Get help</a></div></section>')
(SITE / '.nojekyll').write_text('')
print(f'Generated {len(list(SITE.glob("*.html")))} pages' + (' (release ready)' if args.release_ready else ' (pre-release)'))
