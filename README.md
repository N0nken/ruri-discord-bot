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

<h1>Usage</h1>
<h3>Commands</h3>
<ul>
    <li>
        <h4>/setup</h4>
        <p>Required to run before you can use any of the other commands. Enables the bot for your server. Sets the update channel to whichever channel the command was run in. Can only be run once. See /set_update_channel if you wanna change which channel the bot sends the updates in.</p>
    </li>
    <li>
        <h4>/set_update_channel</h4>
        <p>Run this command in the channel you want the bot to send updates in.</p>
    </li>
    <li>
        <h4>/track</h4>
        <p>Start tracking a manga. The ID is the mangas internal ID on MangaUpdates.com</p>
        <p>To find the mangas id: find the manga on mangaupdates.com then click on "Search for all releases of this series". In the search bar you should see "search=XXXXXXXXX". The number following "search=" is the mangas ID.</p>
    </li>
    <li>
        <h4>/untrack</h4>
        <p>Stops tracking a manga. See /track for manga IDs</p>
    </li>
</ul>
