#!/usr/bin/python
import webapp
import urllib
import os.path


class practica1 (webapp.webApp):

    dic = {}
    dic_inv = {}

    def leerCSV(self):

        fichero = open("urls.csv", "r")
        lineas = fichero.readlines()

        for linea in lineas:
            short_url = linea.split(",")[1]
            short_url = short_url.replace("\n","")
            url = linea.split(",")[0]
            self.dic[int(short_url)] = url
            self.dic_inv[url] = int(short_url)

        fichero.close()


    def escribirCSV(self, url, short_url):

        fichero = open("urls.csv", "a")
        linea = url + "," + str(short_url) + "\n"
        fichero.write(linea)
        fichero.close()


    def parse (self, request):

        # 1. GET http://localhost:1234/
        # 2. GET http://localhost:1234/{numero}
        # 3. POST http://localhost:1234/
        #  body: url
        method = request.split(' ',1)[0]
        resource = request.split(' ',2)[1]
        body = request.split('\r\n\r\n',1)[1]

        return method, resource, body


    def process (self, parsedRequest):

        method, resource, body = parsedRequest # ('GET', '/', '')

        if len(self.dic)==0 and os.path.exists("urls.csv"):
            self.leerCSV()

        print "Acabo de rellenar los diccionarios:"
        for urls in self.dic:
            print str(urls) + "=" + self.dic[urls]
        for urls in self.dic_inv:
            print urls + "=" + str(self.dic_inv[urls])

        if method == "GET":

            number = resource[1:]

            if number == "":
                #si solo es el recurso /
                #   devuelvo el formulario como una pagina html

                htmlAnswer = """
                 <form action="" method="POST">
                    Url:<br>
                    <input type="text" name="url" value=""><br><br>
                    <input type="submit" value="Submit">
                </form>
                """
                httpCode = "200 OK"

            else:
                #si es el recurso /{numero}
                #   devuelvo la pagina html asociada (o pagina de error 404)

                number = int(number)

                if number in self.dic:

                    htmlAnswer = ""
                    httpCode = "302 Found\r\nLocation: " + self.dic[number]

                else:

                    htmlAnswer = "Not found"
                    httpCode = "404 Not Found"

        elif method == "POST":

            #si lleva qs:
            #   aniado http:// si no lo lleva
            #   genero un nuevo numero (el siguiente)
            #   me apunto la correspondencia en los diccionarios
            #   y en el fichero...
            #   devuelvo url = url_acortada

            body = body.split('=',1)[1]
            body = urllib.unquote(body)

            if not (body.startswith("http://") or body.startswith("https://")):
                body = "http://" + body

            short_url = 1 + len(self.dic)
            self.dic[short_url] = body
            self.dic_inv[body] = short_url
            self.escribirCSV(body, short_url)

            htmlAnswer = body + " = " + str(short_url)
            httpCode = "200 OK"

        return httpCode, htmlAnswer

if __name__ == "__main__":
    main = practica1("localhost", 1234)
