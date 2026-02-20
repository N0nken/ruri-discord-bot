<h1>Discord bot for manga updates.</h1>
<p>Uses mangaupdates.com's API to check for new releases.</p>
<p>Requires a MySQL database (see ruri_discord_bot.sql).</p>
<h1>Setup</h1>

<h2>Required bot permissions and intents</h2>
<h3>Permissions</h3>
<ul list-style-type="none">
    <li>Send Messages</li>
    <li>Use Slash Commands</li>
</ul>
<h3>Intents</h3>
<ul list-style-type="none">
    <li>No required intents</li>
</ul>

<h2>MySQL</h2>
See ruri_discord_bot.sql

<h2>.env</h2>
<p>A .env file with the following constants is required</p>
<ul>
    <li>DISCORD_TOKEN=[BOT_TOKEN_HERE]</li>
    <li>SQL_USER=[USERNAME_FOR_MYSQL_DB_HERE]</li>
    <li>SQL_PASS=[PASSWORD_FOR_MYSQL_DB_HERE]</li>
</ul>