#include <stdio.h>
#include <math.h>

// https://math.stackexchange.com/questions/1402362/can-rotations-in-4d-be-given-an-explicit-matrix-form




void
rotation_matrix(double theta, double matrix[2][2]) {
    double offsets[2][2] = {{0, M_PI/2}, {M_PI/-2, 0}}; // cos, -sin, sin, cos

    int i, j;
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            matrix[i][j] = cos(theta + offsets[i][j]);
        }
    }
}

void
rotate_point(double r_m[2][2], double point[4], double result[4]) {
    int i;
    for (i = 0; i < 4; i++) {
        if (i == plane[0]) {
            result[i] = r_m[0][0] * point[plane[0]] + r_m[0][1] * point[plane[1]];
        } else if (i == plane[1]) {
            result[i] = r_m[1][0] * point[plane[0]] + r_m[1][1] * point[plane[1]];
        } else {
            result[i] = point[i];
        }
    }
}

void
rotate(int plane[2], double theta, double points[32][2][4]) {
    double result[32][2][4] = {{{0}}};
    double r_m[2][2] = {{0}};

    rotation_matrix(theta, r_m);

    int i;
    for (i = 0; i < 32; i++) {
        rotate_point(r_m, points[i][0], result[i][0]);
        rotate_point(r_m, points[i][1], result[i][1]);
    }

    memcpy(points, result, sizeof(points));
}


void
rotation(int plane[2], double theta, double point[4], double result[4]) {
    double r_m[2][2] = {{0}};

    rotation_matrix(theta, r_m);

    int i;
    for (i = 0; i < 4; i++) {
        if (i == plane[0]) {
            result[i] = r_m[0][0] * point[plane[0]] + r_m[0][1] * point[plane[1]];
        } else if (i == plane[1]) {
            result[i] = r_m[1][0] * point[plane[0]] + r_m[1][1] * point[plane[1]];
        } else {
            result[i] = point[i];
        }
    }
}

int
main() {
    double point[4] = {1, 1, 1, 1};
    double result[4];
    int plane[2] = {1, 2};

    printf("p: (%f, %f, %f, %f)\n", point[0], point[1], point[2], point[3]);
    printf("---\n");
    rotation(plane, M_PI, point, result);
    printf("r: (%f, %f, %f, %f)\n", result[0], result[1], result[2], result[3]);
    printf("p: (%f, %f, %f, %f)\n", point[0], point[1], point[2], point[3]);
    printf("---\n");
    rotation(plane, M_PI/2, point, result);
    printf("r: (%f, %f, %f, %f)\n", result[0], result[1], result[2], result[3]);
    printf("p: (%f, %f, %f, %f)\n", point[0], point[1], point[2], point[3]);
    printf("---\n");
    rotation(plane, M_PI/4, point, result);
    printf("r: (%f, %f, %f, %f)\n", result[0], result[1], result[2], result[3]);
    printf("p: (%f, %f, %f, %f)\n", point[0], point[1], point[2], point[3]);
    printf("---\n");
}

/*
int
main() {
    double matrix[2][2] = {{1, 2}, {3, 4}};

    int i, j;
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%f ", matrix[i][j]);
        }
        printf("\n");
    }

    // foo(matrix);
    rotation_matrix(0, matrix);

    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%f ", matrix[i][j]);
        }
        printf("\n");
    }
    printf("--\n");

    rotation_matrix(M_PI/2, matrix);

    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%f ", matrix[i][j]);
        }
        printf("\n");
    }
    printf("--\n");

    rotation_matrix(M_PI, matrix);

    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%f ", matrix[i][j]);
        }
        printf("\n");
    }
    printf("--\n");

    rotation_matrix(1.5 * M_PI, matrix);

    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%f ", matrix[i][j]);
        }
        printf("\n");
    }
    printf("--\n");
}
*/
