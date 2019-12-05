#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <getopt.h>

#include <math.h>

char *file_good = NULL;
char *file_bad = NULL;
long size_good = -1;
long size_bad = -1;
double confidence = 0;

int main(int argc, char **argv)
{
    int c;
    int digit_optind = 0;

    while (1) {
        int this_option_optind = optind ? optind : 1;
        int option_index = 0;
        static struct option long_options[] = {
            {"confidence", required_argument, 0, 'c'},
            {"file-good", required_argument, 0, 'g'},
            {"file-bad", required_argument, 0, 'b'},
            {"size-good", required_argument, 0, 0},
            {"size-bad", required_argument, 0, 0},
            {0, 0, 0, 0}
	};

	c = getopt_long(argc, argv, "c:b:g:", long_options, &option_index);
	if (c == -1)
	    break;

	switch (c) {
        case 0:
            if (strcmp(long_options[option_index].name, "size-good") == 0)
            size_good = strtol(optarg, NULL, 10);
            else if (strcmp(long_options[option_index].name, "size-bad") ==
                 0)
            size_bad = strtol(optarg, NULL, 10);
            break;
        case 'c':
            confidence = strtod(optarg, NULL);
            break;

        case 'g':
            file_good = strdup(optarg);
            break;

        case 'b':
            file_bad = strdup(optarg);
            break;

        case '?':
            break;

        default:
            printf("?? getopt returned character code 0%o ??\n", c);
        }
    }

    if (file_good == NULL) {
        fprintf(stderr, "file-good: not specified\n");
        exit(EXIT_FAILURE);
    }

    if (file_bad == NULL) {
        fprintf(stderr, "file-bad: not specified\n");
        exit(EXIT_FAILURE);
    }

    if (size_good < 0) {
        fprintf(stderr, "size-good: not specified\n");
        exit(EXIT_FAILURE);
    }
    if (size_bad < 0) {
        fprintf(stderr, "size-bad: not specified\n");
        exit(EXIT_FAILURE);
    }

    if (confidence <= 0) {
        fprintf(stderr, "confidence: not specified\n");
        exit(EXIT_FAILURE);
    }

    FILE *fd_good = fopen(file_good, "r");
    unsigned long count, length, sequences;
    double sum_good = 0, sum_bad = 0, method_moments = 0;
    double non_scaled_sum_good = 0, non_scaled_sum_bad = 0;
    double mult_good = 1, mult_bad = 1;
    double P_leq_X = 0, P_geq_X = 1;

    sequences = 0;
    while (fscanf(fd_good, "%lu %lu", &count, &length) == 2) {
        double P_eq_X = ((double) count) / ((double) size_good);
        P_leq_X += P_eq_X;
        double p = (1 - exp(log(1 - confidence) / (1 + (double) length)));
        double tot = p * P_eq_X;
        sequences++;
        P_geq_X -= P_eq_X;
        fprintf(stdout,
            "file_good: length %lu count %lu p %f P_eq_X %f P_leq_X %f P_geq_X %f Tot %f\n",
            length, count, p, P_eq_X, P_leq_X, P_geq_X, tot);
        sum_good += tot;
        non_scaled_sum_good += tot;
        mult_good *= tot;
        method_moments += (count * length);
    }

    // sum_good = (double) sum_good / (double) sequences;
    sum_good = (double) sum_good / (double) size_good;
    fclose(fd_good);

    FILE *fd_bad = fopen(file_bad, "r");

    P_geq_X = 1;
    P_leq_X = 0;
    sequences = 0;
    while (fscanf(fd_bad, "%lu %lu", &count, &length) == 2) {
        double P_eq_X = ((double) count) / ((double) size_bad);
        P_leq_X += P_eq_X;
        double p = 1 - exp(2 * log(1 - confidence) / (1 + (double) length));

        double tot = p * P_eq_X;
        sequences++;
        P_geq_X -= P_eq_X;
        fprintf(stdout,
            "file_bad: length %lu count %lu p %f P_eq_X %f P_leq_X %f P_geq_X %f Tot %f\n",
            length, count, p, P_eq_X, P_leq_X, P_geq_X, tot);
        sum_bad += tot;
        non_scaled_sum_bad += tot;
        mult_bad *= tot;
    }

    sum_bad = (double) sum_bad / (double) sequences;
    fclose(fd_bad);

    fprintf(stdout, "method_moments %f %f || sum_good %f non_scaled_sum_good %f mult_good %f || sum_bad %f non_scaled_sum_bad %f mult_bad %f\n", method_moments, 1/method_moments, sum_good, non_scaled_sum_good, mult_good, sum_bad, non_scaled_sum_bad, mult_bad);

    if (non_scaled_sum_good > non_scaled_sum_bad) {
        fprintf (stdout, "FAILURE - non_scaled_sum_good %f > non_scaled_sum_bad %f\n", non_scaled_sum_good, non_scaled_sum_bad);
        exit (EXIT_FAILURE);
    } else {
        int len = (int) floor (log (1 - confidence)/log (non_scaled_sum_good));
        fprintf (stdout, "SUCCESS - len %d\n", len);
    }
    exit(EXIT_SUCCESS);
}
