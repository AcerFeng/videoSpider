
class HtmlOutPuter(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas = data

    def output_html(self):
        fout = open('output.html', 'w')

        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['name'])
            fout.write("<td>%s</td>" % data['desc'])
            fout.write("<td>%s</td>" % data['play_number'])
            fout.write("<td>%s</td>" % data['update_status'])
            fout.write("<td>%s</td>" % data['image'])
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()