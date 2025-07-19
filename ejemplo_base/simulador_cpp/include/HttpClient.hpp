#pragma once
#include <string>

class HttpClient {
private:
    std::string token;
    std::string url;

public:
    HttpClient(const std::string& token);
    bool enviarJson(const std::string& payload);
};
