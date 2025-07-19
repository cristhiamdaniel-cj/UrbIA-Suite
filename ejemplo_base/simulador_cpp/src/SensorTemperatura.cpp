#include "SensorTemperatura.hpp"
#include <random>

SensorTemperatura::SensorTemperatura() : SensorBase("temperatura") {}

std::string SensorTemperatura::getTipo() const {
    return "temperatura";
}

double SensorTemperatura::leerValor() const {
    static std::default_random_engine gen(std::random_device{}());
    std::uniform_int_distribution<int> chance(1,100);
    if (chance(gen) <= 90) {
        // 20–35 °C
        std::uniform_real_distribution<double> dist(20.0, 35.0);
        return dist(gen);
    } else {
        // fuera de rango alto 35–45 °C
        std::uniform_real_distribution<double> out(35.1, 45.0);
        return out(gen);
    }
}
