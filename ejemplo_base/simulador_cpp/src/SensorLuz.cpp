#include "SensorLuz.hpp"
#include <random>

SensorLuz::SensorLuz() : SensorBase("luz") {}

std::string SensorLuz::getTipo() const {
    return "luz";
}

double SensorLuz::leerValor() const {
    static std::default_random_engine gen(std::random_device{}());
    std::uniform_int_distribution<int> chance(1,100);
    if (chance(gen) <= 90) {
        // 0–1000 lux
        std::uniform_real_distribution<double> dist(0.0, 1000.0);
        return dist(gen);
    } else {
        // fuera de rango alto 1000–1300 lux
        std::uniform_real_distribution<double> out(1000.1, 1300.0);
        return out(gen);
    }
}
