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
<p>A MySQL database is required for this branch. If you don't have access to one then the main branch (which uses local .json files) should be used instead.</p>
<p>For the database design see ruri_discord_bot.sql.</p>

<h3>.env</h3>
<p>A .env file with the following constants is required</p>
<ul>
    <li>DISCORD_TOKEN=[BOT_TOKEN_HERE]</li>
    <li>SQL_USER=[USERNAME_FOR_MYSQL_DB_HERE]</li>
    <li>SQL_PASS=[PASSWORD_FOR_MYSQL_DB_HERE]</li>
</ul>