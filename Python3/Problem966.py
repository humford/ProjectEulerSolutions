import hashlib
import os
import shutil
import subprocess
import tempfile
import time


TARGET = 200


CPP_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Point {
    double x;
    double y;
};

Point operator+(const Point& left, const Point& right) {
    return {left.x + right.x, left.y + right.y};
}

Point operator-(const Point& left, const Point& right) {
    return {left.x - right.x, left.y - right.y};
}

Point operator*(const Point& point, double scalar) {
    return {point.x * scalar, point.y * scalar};
}

double dot(const Point& left, const Point& right) {
    return left.x * right.x + left.y * right.y;
}

double cross(const Point& left, const Point& right) {
    return left.x * right.y - left.y * right.x;
}

double norm(const Point& point) {
    return std::sqrt(std::max(0.0, dot(point, point)));
}

constexpr double EPSILON = 1e-12;
const double PI = std::acos(-1.0);

std::vector<double> segmentCircleIntersections(
    const Point& start,
    const Point& end,
    double radius
) {
    Point delta = end - start;
    double quadratic = dot(delta, delta);
    std::vector<double> intersections;

    if (quadratic < 1e-18) {
        return intersections;
    }

    double linear = 2.0 * dot(start, delta);
    double constant = dot(start, start) - radius * radius;
    double discriminant = linear * linear - 4.0 * quadratic * constant;

    if (discriminant < -EPSILON) {
        return intersections;
    }
    if (discriminant < 0.0) {
        discriminant = 0.0;
    }

    double root = std::sqrt(discriminant);
    for (double value : {
             (-linear - root) / (2.0 * quadratic),
             (-linear + root) / (2.0 * quadratic),
         }) {
        if (value >= -EPSILON && value <= 1.0 + EPSILON) {
            value = std::min(1.0, std::max(0.0, value));
            if (
                intersections.empty()
                || std::abs(value - intersections.back()) > EPSILON
            ) {
                intersections.push_back(value);
            }
        }
    }

    std::sort(intersections.begin(), intersections.end());
    return intersections;
}

double edgeIntersectionContribution(
    const Point& start,
    const Point& end,
    double radius
) {
    if (norm(start) <= radius + EPSILON && norm(end) <= radius + EPSILON) {
        return 0.5 * cross(start, end);
    }

    std::vector<Point> points = {start};
    for (double t : segmentCircleIntersections(start, end, radius)) {
        Point intersection = start + (end - start) * t;
        if (norm(intersection - points.back()) > EPSILON) {
            points.push_back(intersection);
        }
    }
    if (norm(points.back() - end) > EPSILON) {
        points.push_back(end);
    }

    double total = 0.0;
    for (std::size_t index = 0; index + 1 < points.size(); ++index) {
        Point left = points[index];
        Point right = points[index + 1];
        Point midpoint = (left + right) * 0.5;

        if (norm(midpoint) <= radius + EPSILON) {
            total += 0.5 * cross(left, right);
        } else {
            double angle = std::atan2(cross(left, right), dot(left, right));
            total += 0.5 * radius * radius * angle;
        }
    }

    return total;
}

double triangleCircleIntersection(
    const std::vector<Point>& triangle,
    const Point& center,
    double radius
) {
    double total = 0.0;
    for (int index = 0; index < 3; ++index) {
        total += edgeIntersectionContribution(
            triangle[index] - center,
            triangle[(index + 1) % 3] - center,
            radius
        );
    }
    return std::abs(total);
}

std::vector<Point> triangleFromSides(int sideA, int sideB, int sideC) {
    Point a = {0.0, 0.0};
    Point b = {static_cast<double>(sideC), 0.0};
    double x =
        (static_cast<double>(sideB) * sideB
         + static_cast<double>(sideC) * sideC
         - static_cast<double>(sideA) * sideA)
        / (2.0 * sideC);
    double ySquared = static_cast<double>(sideB) * sideB - x * x;
    Point c = {x, std::sqrt(std::max(0.0, ySquared))};
    return {a, b, c};
}

double triangleArea(const std::vector<Point>& triangle) {
    return std::abs(0.5 * cross(triangle[1] - triangle[0], triangle[2] - triangle[0]));
}

Point centroid(const std::vector<Point>& triangle) {
    return {
        (triangle[0].x + triangle[1].x + triangle[2].x) / 3.0,
        (triangle[0].y + triangle[1].y + triangle[2].y) / 3.0,
    };
}

Point incenter(const std::vector<Point>& triangle) {
    double sideA = norm(triangle[1] - triangle[2]);
    double sideB = norm(triangle[0] - triangle[2]);
    double sideC = norm(triangle[0] - triangle[1]);
    double perimeter = sideA + sideB + sideC;
    return {
        (sideA * triangle[0].x + sideB * triangle[1].x + sideC * triangle[2].x)
            / perimeter,
        (sideA * triangle[0].y + sideB * triangle[1].y + sideC * triangle[2].y)
            / perimeter,
    };
}

bool circumcenter(const std::vector<Point>& triangle, Point& center) {
    Point a = triangle[0];
    Point b = triangle[1];
    Point c = triangle[2];
    double determinant =
        2.0
        * (
            a.x * (b.y - c.y)
            + b.x * (c.y - a.y)
            + c.x * (a.y - b.y)
        );

    if (std::abs(determinant) < 1e-15) {
        return false;
    }

    center = {
        (
            (a.x * a.x + a.y * a.y) * (b.y - c.y)
            + (b.x * b.x + b.y * b.y) * (c.y - a.y)
            + (c.x * c.x + c.y * c.y) * (a.y - b.y)
        ) / determinant,
        (
            (a.x * a.x + a.y * a.y) * (c.x - b.x)
            + (b.x * b.x + b.y * b.y) * (a.x - c.x)
            + (c.x * c.x + c.y * c.y) * (b.x - a.x)
        ) / determinant,
    };
    return true;
}

double maximalIntersection(int sideA, int sideB, int sideC) {
    std::vector<Point> triangle = triangleFromSides(sideA, sideB, sideC);
    double area = triangleArea(triangle);
    double radius = std::sqrt(area / PI);

    double minX = std::min({triangle[0].x, triangle[1].x, triangle[2].x}) - 2.0 * radius;
    double maxX = std::max({triangle[0].x, triangle[1].x, triangle[2].x}) + 2.0 * radius;
    double minY = std::min({triangle[0].y, triangle[1].y, triangle[2].y}) - 2.0 * radius;
    double maxY = std::max({triangle[0].y, triangle[1].y, triangle[2].y}) + 2.0 * radius;

    std::vector<Point> starts = {
        centroid(triangle),
        incenter(triangle),
        triangle[0],
        triangle[1],
        triangle[2],
        (triangle[0] + triangle[1]) * 0.5,
        (triangle[1] + triangle[2]) * 0.5,
        (triangle[2] + triangle[0]) * 0.5,
    };

    Point circum;
    if (circumcenter(triangle, circum)) {
        starts.push_back(circum);
    }

    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            double xFraction = (i + 0.5) / 5.0;
            double yFraction = (j + 0.5) / 5.0;
            starts.push_back({
                minX + xFraction * (maxX - minX),
                minY + yFraction * (maxY - minY),
            });
        }
    }

    Point center = centroid(triangle);
    for (int direction = 0; direction < 16; ++direction) {
        double angle = 2.0 * PI * direction / 16.0;
        for (int step = 0; step <= 4; ++step) {
            double distance = (step / 4.0) * 2.0 * radius;
            starts.push_back({
                center.x + distance * std::cos(angle),
                center.y + distance * std::sin(angle),
            });
        }
    }

    std::uint64_t seed = 123456789ULL;
    for (int index = 0; index < 250; ++index) {
        seed = seed * 6364136223846793005ULL + 1442695040888963407ULL;
        double xFraction =
            static_cast<double>(seed & 0xffffffffULL)
            / static_cast<double>(0xffffffffULL);
        seed = seed * 6364136223846793005ULL + 1442695040888963407ULL;
        double yFraction =
            static_cast<double>((seed >> 16) & 0xffffffffULL)
            / static_cast<double>(0xffffffffULL);
        starts.push_back({
            minX + xFraction * (maxX - minX),
            minY + yFraction * (maxY - minY),
        });
    }

    auto evaluate = [&](const Point& point) {
        return triangleCircleIntersection(triangle, point, radius);
    };

    double bestValue = -1.0;
    Point bestCenter = center;
    for (Point start : starts) {
        start.x = std::min(maxX, std::max(minX, start.x));
        start.y = std::min(maxY, std::max(minY, start.y));
        double value = evaluate(start);
        if (value > bestValue) {
            bestValue = value;
            bestCenter = start;
        }
    }

    const std::vector<Point> directions = {
        {0.0, 0.0},
        {1.0, 0.0},
        {-1.0, 0.0},
        {0.0, 1.0},
        {0.0, -1.0},
        {1.0, 1.0},
        {-1.0, 1.0},
        {1.0, -1.0},
        {-1.0, -1.0},
    };

    double step = std::max({maxX - minX, maxY - minY, radius});
    while (step > 1e-7) {
        bool improved = false;
        for (const Point& direction : directions) {
            Point candidate = {
                std::min(maxX, std::max(minX, bestCenter.x + direction.x * step)),
                std::min(maxY, std::max(minY, bestCenter.y + direction.y * step)),
            };
            double value = evaluate(candidate);
            if (value > bestValue + 1e-12) {
                bestValue = value;
                bestCenter = candidate;
                improved = true;
            }
        }
        if (!improved) {
            step *= 0.5;
        }
    }

    return bestValue;
}

double sumIntersections(int perimeterLimit) {
    double total = 0.0;

    for (int sideA = 1; sideA <= perimeterLimit; ++sideA) {
        for (int sideB = sideA; sideB <= perimeterLimit; ++sideB) {
            int maxSideC = std::min(sideA + sideB - 1, perimeterLimit - sideA - sideB);
            for (int sideC = sideB; sideC <= maxSideC; ++sideC) {
                total += maximalIntersection(sideA, sideB, sideC);
            }
        }
    }

    return total;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        return 2;
    }

    std::string mode = argv[1];
    std::cout.setf(std::ios::fixed);

    if (mode == "I" && argc == 5) {
        int sideA = std::atoi(argv[2]);
        int sideB = std::atoi(argv[3]);
        int sideC = std::atoi(argv[4]);
        std::cout << std::setprecision(12)
                  << maximalIntersection(sideA, sideB, sideC)
                  << "\n";
        return 0;
    }

    if (mode == "sum" && argc == 3) {
        int perimeterLimit = std::atoi(argv[2]);
        std::cout << std::setprecision(12)
                  << sumIntersections(perimeterLimit)
                  << "\n";
        return 0;
    }

    return 2;
}
"""


def nativeExecutable():
    compiler = shutil.which("c++") or shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        raise RuntimeError("Problem 966 requires a C++ compiler for the geometry kernel.")

    digest = hashlib.sha256(CPP_SOURCE.encode("utf-8")).hexdigest()[:16]
    base = os.path.join(tempfile.gettempdir(), "project_euler_966_" + digest)
    sourcePath = base + ".cpp"
    executablePath = base

    if not os.path.exists(executablePath):
        with open(sourcePath, "w", encoding="utf-8") as source:
            source.write(CPP_SOURCE)
        subprocess.run(
            [compiler, "-O3", "-std=c++17", sourcePath, "-o", executablePath],
            check=True,
        )

    return executablePath


def runNative(*arguments):
    completed = subprocess.run(
        [nativeExecutable(), *map(str, arguments)],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(completed.stdout.strip())


def I(sideA, sideB, sideC):
    return runNative("I", sideA, sideB, sideC)


def sumIntersections(perimeterLimit):
    return runNative("sum", perimeterLimit)


def solve():
    return sumIntersections(TARGET)


def runTests():
    assert abs(I(3, 4, 5) - 4.593049) < 5e-7
    assert abs(I(3, 4, 6) - 3.552564) < 5e-7


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + format(answer, ".2f") + " in " + str(elapsed) + " seconds.")
