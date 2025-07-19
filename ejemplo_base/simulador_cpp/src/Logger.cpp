#include "Logger.hpp"
#include <fstream>
#include <ctime>

void Logger::log(const std::string& mensaje) {
    std::ofstream archivo("logs/simulador.log", std::ios_base::app);
    if (archivo.is_open()) {
        std::time_t ahora = std::time(nullptr);
        char* tiempo = std::ctime(&ahora);
        if (tiempo) {
            tiempo[std::char_traits<char>::length(tiempo) - 1] = '\0';  // Eliminar \n
            archivo << "[" << tiempo << "] " << mensaje << std::endl;
        }
    }
}
