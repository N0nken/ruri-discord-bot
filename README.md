<h1>Discord bot for manga updates.</h1>
<p>Uses mangaupdates.com's API to check for new releases.</p>
<p>Requires a MySQL database (see ruri_discord_bot.sql).</p>
<h1>Setup</h1>

<h3>Discord bot</h3>
<h5>Required permissions</h5>
<ul list-style-type="none">
    <li>Send Messages</li>
    <li>Use Slash Commands</li>
</ul>
<h5>Required intents</h5>
<ul list-style-type="none">
    <li>No required intents</li>
</ul>

<h3>MySQL</h3>
<p>A MySQL database is required.</p>
<p>For the database design see ruri_discord_bot.sql.</p>

<h3>.env</h3>
<p>Fill out template.env with appropriate values and rename it to .env.</p>