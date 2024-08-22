class HtmlPhoto():
    def __init__(self):
        self.html_doc = list()
        self.html_table = dict()
        self._row_count = 0
        self.setup_table()

    def setup_table(self):
        table_head = '<tr><th scope="col">id</th><th scope="col">name_1</th><th scope="col">name_2</th><th scope="col">photo</th></tr>'
        self.html_table["start"] = "<table>"
        self.html_table["end"] = "</table>"
        self.html_table["head"] = table_head
        self.html_table["row"] = list()

    def add_table_row(self, id_field, name_1, name_2, photobase64, photoencoding=None):
        if not photoencoding:
            photoencoding = "jpg;base64"
        photo_img = f'<img src="data:image/{photoencoding},{photobase64}" alt="{id_field}-{name_1}-{name_2}">'
        table_row = f'<tr><th scope="row">{id_field}</th><td>{name_1}</td><td>{name_2}</td><td>{photo_img}</td></tr>'
        self.html_table["row"].append(table_row)
        self._row_count += 1

    @property
    def row_count(self):
        return self._row_count

    def begin_html(self):
        self.html_doc.append("<!doctype html>")
        self.html_doc.append("<html>")
        self.html_doc.append("<head>")
        self.html_doc.append("<title>VCF Photos</title>")
        self.html_doc.append("""<style>
 body {background-color: powderblue;}

 th,
 td {
   border: 1px solid rgb(160 160 160);
   padding: 3px 2px;
 }

 th[scope='col'] {
   background-color: #505050;
   color: #fff;
 }

 th[scope='row'] {
   background-color: #d6ecd4;
 }

 td {
   text-align: center;
 }

 tr:nth-of-type(even) {
   background-color: #eee;
 }

 table {
   border-collapse: collapse;
   border: 2px solid rgb(140 140 140);
   font-family: sans-serif;
   font-size: 0.8rem;
   letter-spacing: 1px;
 }

 </style>""")
        self.html_doc.append("</head>")
        self.html_doc.append("<body>")

    def end_html(self):
        self.html_doc.append("</body>")
        self.html_doc.append("</html>")

    def write_html(self, html_out_filename):
        self.begin_html()
        # add table to html
        self.html_doc.append(self.html_table["start"])
        self.html_doc.append(self.html_table["head"])
        for t_row in self.html_table["row"]:
            self.html_doc.append(t_row)
        self.html_doc.append(self.html_table["end"])
        self.end_html()
        with open(html_out_filename, "wt") as h_file:
            for html_line in self.html_doc:
                h_file.write(html_line+"\n")
