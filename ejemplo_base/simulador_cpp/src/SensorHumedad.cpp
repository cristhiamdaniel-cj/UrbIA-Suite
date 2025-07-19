#include "SensorHumedad.hpp"
#include <random>

SensorHumedad::SensorHumedad() : SensorBase("humedad") {}

std::string SensorHumedad::getTipo() const {
    return "humedad";
}

double SensorHumedad::leerValor() const {
    static std::default_random_engine gen(std::random_device{}());
    std::uniform_int_distribution<int> chance(1,100);
    if (chance(gen) <= 90) {
        // 40–80 %
        std::uniform_real_distribution<double> dist(40.0, 80.0);
        return dist(gen);
    } else {
        // fuera de rango alto 80–100 %
        std::uniform_real_distribution<double> out(80.1, 100.0);
        return out(gen);
    }
}
