#include <stdio.h>
#include <string.h>
#include <math.h>

// https://math.stackexchange.com/questions/1402362/can-rotations-in-4d-be-given-an-explicit-matrix-form

static double g_corners[16][4] = {{1,1,1,1},{1,1,1,-1},{1,1,-1,1},{1,1,-1,-1},{1,-1,1,1},{1,-1,1,-1},{1,-1,-1,1},{1,-1,-1,-1},{-1,1,1,1},{-1,1,1,-1},{-1,1,-1,1},{-1,1,-1,-1},{-1,-1,1,1},{-1,-1,1,-1},{-1,-1,-1,1},{-1,-1,-1,-1}};
static int g_lines[32][2];
static double g_lines3d[32][2][3];

void
init_lines() {
    int line_idx = 0;
    int p1;
    for (p1 = 0; p1 < 16; p1++) {
        int p2;
        for (p2 = p1; p2 < 16; p2++) {
            if (p1 == p2) continue;
            int i;
            int c = 0;
            for (i = 0; i < 4; i++) {
                if (g_corners[p1][i] == g_corners[p2][i]) {
                    c++;
                }
            }
            if ( c == 3 ) {
                g_lines[line_idx][0] = p1;
                g_lines[line_idx][1] = p2;
                line_idx++;
            }
        }
    }
}

void
print_corners() {
    int i;
    for (i = 0; i < 16; i++) {
        int j;
        printf("(");
        for (j = 0; j < 4; j++) {
            if (j != 0) {
                printf(" ");
            }
            printf("%f", g_corners[i][j]);
        }
        printf(")\n");
    }
}

void
print_lines3d() {
    int i;
    for (i = 0; i < 32; i++) {
        int a;
        for (a = 0; a < 2; a++) {
            printf("("); fflush(0);
            int j;
            for (j = 0; j < 3; j++) {
                if (j != 0) {
                    printf(" ");
                }
                printf("%f", g_lines3d[i][a][j]);
            }
            printf(") ");
        }
        printf("\n");
    }
}

void
print_lines() {
    int i;
    for (i = 0; i < 32; i++) {
        int a;
        for (a = 0; a < 2; a++) {
            printf("("); fflush(0);
            int j;
            for (j = 0; j < 4; j++) {
                if (j != 0) {
                    printf(" ");
                }
                printf("%f", g_corners[g_lines[i][a]][j]);
            }
            printf(") ");
        }
        printf("\n");
    }
}

static void
double_rotation_matrix(double alpha, double beta, double matrix[4][4]) {
    /*
     * Rotation Matrix:
     *   cos a   0  -sin a   0
     *     0   cos b   0  -sin b
     *   sin a   0   cos a   0
     *    0    sin b   0   cos b
     */
    double offsets[3] = {M_PI/2, 0, M_PI/-2}; // -sin cos sin
    double *angles[2] = {&alpha, &beta};

    int i;
    for (i = 0; i < 4; i++) {
        int j;
        for (j = 0; j < 4; j++) {
            if (!(i % 2) ^ (j % 2)) {
                matrix[i][j] = cos(*(angles[i%2]) + offsets[((i-j)/2)+1]);
            } else {
                matrix[i][j] = 0;
            }
        }
    }
}

static void
double_rotate_point(double drm[4][4], double point[4], double result[4]) {
    result[0] = 0;
    result[1] = 0;
    result[2] = 0;
    result[3] = 0;

    int i;
    for (i = 0; i < 4; i++) {
        int j;
        for (j = 0; j < 4; j++) {
            result[i] += drm[i][j] * point[j];
        }
    }
}

static void
double_rotate(double alpha, double beta, double points[16][4]) {
    double result[16][4] = {{0}};
    double drm[4][4] = {{0}};

    double_rotation_matrix(alpha, beta, drm);

    int i;
    for (i = 0; i < 16; i++) {
        double_rotate_point(drm, points[i], result[i]);
    }
    memcpy(points, result, sizeof(double) * 16 * 4);
}

static void
project_point(double point[4], double proj[3], double h) {
    proj[0] = point[0] / (h - point[3]);
    proj[1] = point[1] / (h - point[3]);
    proj[2] = point[2] / (h - point[3]);
}

static void
project(double points[16][4], double projs[16][3], double h) {
    int i;
    for (i = 0; i < 16; i++) {
        project_point(points[i], projs[i], h);
    }
}

static void
fill_line3d(int line_idx[32][2], double lines[32][2][3], double points[16][3]) {
    int i, p, c;
    for (i = 0; i < 32; i++) {
        for (p = 0; p < 2; p++) {
            for (c = 0; c < 3; c++) {
                lines[i][p][c] = points[line_idx[i][p]][c];
            }
        }
    }
}

void
do_rotation(double alpha, double beta, double height) {
    double points3d[16][3] = {{0}};

    double_rotate(alpha, beta, g_corners);

    project(g_corners, points3d, height);

    fill_line3d(g_lines, g_lines3d, points3d);
}

double
get(int i, int j, int k) {
    return g_lines3d[i][j][k];
}
