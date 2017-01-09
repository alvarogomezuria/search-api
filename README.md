# search-api
Deploy the app: $ gcloud app deploy --version searching <br>
*Input: <br>
{"first_name": "Josep",    "last_name": "Mic", "company_name": "Hollywood"},<br>
{"first_name": "Jacob Mic",    "last_name": "Moc", "company_name": None},<br>
{"first_name": "Julia",    "last_name": "Muc", "company_name": "Zync Mic"},<br>
{"first_name": "Jessy",    "last_name": "Mac", "company_name": "Alphabet Mic"},<br>
{"first_name": "Julia Mic",    "last_name": "Mac", "company_name": None},<br>
{"first_name": "Jessy Mic",    "last_name": "Mac", "company_name": "Alphabet Mic"},
<br><br>
*Output:<br>
{"first_name": "Jessy",    "last_name":  "Mac", "company_name": "Alphabet Mic"},<br>
{"first_name": "Jessy Mic", "last_name": "Mac", "company_name": "Alphabet Mic"},<br>
{"first_name": "Josep",     "last_name": "Mic", "company_name": "Hollywood"},<br>
{"first_name": "Julia Mic", "last_name": "Mac", "company_name": None},<br>
{"first_name": "Jacob Mic", "last_name": "Moc", "company_name": None},<br>
{"first_name": "Julia",     "last_name": "Muc", "company_name": "Zync Mic"}
