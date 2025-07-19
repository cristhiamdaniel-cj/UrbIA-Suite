#include "SensorCO2.hpp"
#include <random>

SensorCO2::SensorCO2() : SensorBase("co2") {}

std::string SensorCO2::getTipo() const {
    return "co2";
}

double SensorCO2::leerValor() const {
    static std::default_random_engine gen(std::random_device{}());
    // 90%: 300–800 ppm
    std::uniform_int_distribution<int> chance(1,100);
    if (chance(gen) <= 90) {
        std::uniform_real_distribution<double> dist(300.0, 800.0);
        return dist(gen);
    } else {
        // 10%: fuera de rango alto 800–1000 ppm
        std::uniform_real_distribution<double> out(800.1, 1000.0);
        return out(gen);
    }
}
