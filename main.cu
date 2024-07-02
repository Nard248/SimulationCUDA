#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <thrust/complex.h>
#include "parameters.h"



int main() {
    std::cout << "Initializing random seed..." << std::endl;
    std::srand(20);

    // Example parameter initialization
    std::tuple<float, float, float> d = { 0.03f, 90.0f / 600.0f, 90.0f / 600.0f };
    std::tuple<int, int, int> N = { 200, 600, 600 };
    std::tuple<int, int, int> myu_size = { 5, 8, 8 };
    std::tuple<float, float> myu_mstd = { 5.4f, 0.8f };

    std::cout << "Initializing parameters..." << std::endl;
    Params params = initialize_parameters(d, N, myu_size, myu_mstd);

    std::cout << "Computing myu..." << std::endl;
    compute_myu(params);

    std::cout << "Computing state..." << std::endl;
    compute_state(params.d_myu, params);

    std::cout << "Printing parameters..." << std::endl;
    print_parameters(params);

    std::cout << "Freeing allocated memory..." << std::endl;
    free_parameters(params);

    std::cout << "Program completed successfully!" << std::endl;

    return 0;
}

