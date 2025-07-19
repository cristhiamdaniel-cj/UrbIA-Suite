#include "EnvLoader.hpp"
#include <fstream>
#include <sstream>

std::string getEnvVar(const std::string& key) {
    std::ifstream file(".env");
    std::string line;
    while (std::getline(file, line)) {
        if (line.find(key + "=") == 0) {
            return line.substr(key.length() + 1);
        }
    }
    return "";
}
