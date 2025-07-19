#include "HttpClient.hpp"
#include <curl/curl.h>
#include <iostream>

HttpClient::HttpClient(const std::string& token)
    : token(token), url("https://inti-data.ngrok.io/api/v1/" + token + "/telemetry") {}



bool HttpClient::enviarJson(const std::string& payload) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "❌ Error: No se pudo inicializar CURL.\n";
        return false;
    }

    // Agregar los encabezados HTTP para el contenido JSON
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    // Establecer las opciones para la solicitud CURL
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);  // Incrementar el tiempo de espera a 30 segundos

    // Realizar la solicitud POST
    CURLcode res = curl_easy_perform(curl);

    // Comprobar si hubo algún error al hacer la solicitud
    if (res != CURLE_OK) {
        std::cerr << "❌ Error de CURL: " << curl_easy_strerror(res) << std::endl;

        // Obtener el código de respuesta HTTP
        long response_code;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
        std::cerr << "Código de respuesta HTTP: " << response_code << std::endl;

        // Liberar los recursos de CURL
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
        return false;
    }

    // Obtener el código de respuesta HTTP si la solicitud fue exitosa
    long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code == 200) {
        std::cout << "✅ Datos enviados correctamente. Código de respuesta: " << response_code << std::endl;
    } else {
        std::cerr << "❌ Error al enviar datos. Código de respuesta: " << response_code << std::endl;
    }

    // Liberar los recursos de CURL
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    return true;
}
