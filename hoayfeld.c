/**
 *
 * Small piece of code for computing E[x], considering Hoayfeld's
 * methodology. You might remember the equation,
 *
 * E[x] = N * h_{N} / (L * B),
 *
 * where L is the size of the peer list, B is the number of bootstrap
 * entities, and N the number of users in the system (h_{N} is the
 * n-th harmonic number). E[x] is the expected number of queries
 * to obtain a full snapshot of the system with high probability.
 * 
 * The piece of code is more powerul actually: it can compute a given
 * harmonic number (--action comp-hnum) or a list of harmornic
 * numbers (--action list-hnum). It can also compute either E[x], N
 * (and h_{N}), L, or B, given the other parameters. You just need to
 * specify the proper action (see --help).
 *
 * Some use cases:
 *     ./hoayfeld --help
 *     ./hoayfeld --action list-hnum --hnum-begin 5 --hnum-end 10
 *     ./hoayfeld --action comp-hnum --hnum 10
 *     ./hoayfeld --action comp-e-est --num-users 4000 --list-max 200 --num-boot 4
 *     ./hoayfeld --action comp-num-users --e-est 44.356951 --list-max 200 --num-boot 4
 *     ./hoayfeld --action comp-list-max --e-est 44.356951 --num-users 4000 --num-boot 4
 *     ./hoayfeld --action comp-num-boot --e-est 44.356951 --num-users 4000 --list-max 200
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <math.h>
#include <getopt.h>

#define MAX_LOOP                          500000

#define ACTION_COMPUTE_E_EST              1
#define ACTION_COMPUTE_NUM_USERS          2
#define ACTION_COMPUTE_LIST_MAX           3
#define ACTION_COMPUTE_NUM_BOOT           4

#define PARAM_E_EST                       0x01
#define PARAM_NUM_USERS                   0x02
#define PARAM_LIST_MAX                    0x04
#define PARAM_NUM_BOOT                    0x08
double e_est;
double num_users;
double list_max;
double num_boot;

#define ACTION_LIST_HARMONIC_NUM          5

#define PARAM_NUM_HARM_BEGIN              0x10
#define PARAM_NUM_HARM_END                0x20
double num_harm_begin;
double num_harm_end;

#define ACTION_COMP_HARMONIC_NUM          6

#define PARAM_NUM_HARM_COMPUTE            0x40
double num_harm_compute;

struct __action {
    char *name;
    int code;
};

double compute_harmonic_num(double number, int print)
{
    double h = 1;
    int i;

    for (i = 2; i <= (int) number; i++)
	h += 1 / ((double) i);
    if (print)
	fprintf(stdout, "%.0f harmonic_num_is %f\n", number, h);
    return h;
}

void compute_harmonic_num_list(double begin, double end)
{
    double h = 0;
    int i;

    for (i = 1; i < (int) begin; i++)
	h += 1 / ((double) i);
    for (i = (int) begin; i <= (int) end; i++) {
	h += 1 / ((double) i);
	fprintf(stdout, "%d harmonic_num_is %f\n", i, h);
    }
}

void compute_num_users(double e_est, double list_max, double num_boot)
{
    double rst = e_est * list_max * num_boot;
    double h = 1, prev, curr;
    int i;

    if (h == (rst)) {
	fprintf(stdout, "exact: num-users %f hnum %f\n", h, h);
    } else {
	for (i = 2; i < MAX_LOOP; i++) {
	    prev = h;
	    h += 1 / ((double) i);
	    curr = h * ((double) i);
	    if (curr == rst) {
		fprintf(stdout, "exact: num-users %f hnum %f\n", h, h);
		break;
	    } else if (curr > rst) {
		fprintf(stdout, "prev: num-users %f hnum %f\n",
			(double) (i - 1), prev);
		fprintf(stdout, "curr: num-users %f hnum %f\n", (double) i,
			h);
		break;
	    }
	}
	if (i == MAX_LOOP) {
	    fprintf(stderr, "MAX_LOOP reached; no result found\n");
	    exit(1);
	}
    }
}

void compute_e_est(double num_users, double list_max, double num_boot)
{
    double e_est, hnum;

    hnum = compute_harmonic_num(num_users, 0);
    e_est = num_users * hnum / (list_max * num_boot);
    fprintf(stdout, "e-est %f ( hnum %f )\n", e_est, hnum);
}

void compute_list_max(double e_est, double num_users, double num_boot)
{
    double list_max, hnum;

    hnum = compute_harmonic_num(num_users, 0);
    list_max = num_users * hnum / (e_est * num_boot);
    fprintf(stdout, "list-max %f ( hnum %f )\n", list_max, hnum);
}

void compute_num_boot(double e_est, double num_users, double list_max)
{
    double num_boot, hnum;

    hnum = compute_harmonic_num(num_users, 0);
    num_boot = num_users * hnum / (e_est * list_max);
    fprintf(stdout, "num-boot %f ( hnum %f )\n", num_boot, hnum);
}

int main(int argc, char **argv)
{
    int c;
    int digit_optind = 0;
    unsigned int param_ok = 0;
    int action = -1;

    while (1) {
	int this_option_optind = optind ? optind : 1;
	int option_index = 0;
	char *endptr;
	static struct option long_options[] = {
	    {"e-est", required_argument, 0, 'e'},
	    {"num-users", required_argument, 0, 'n'},
	    {"list-max", required_argument, 0, 'l'},
	    {"num-boot", required_argument, 0, 'b'},
	    {"action", required_argument, 0, 'a'},
	    {"hnum-begin", required_argument, 0, 1},
	    {"hnum-end", required_argument, 0, 2},
	    {"hnum", required_argument, 0, 3},
	    {"help", no_argument, 0, 'h'},
	    {0, 0, 0, 0}
	};

	static struct __action actions[] = {
	    {"comp-e-est", ACTION_COMPUTE_E_EST},
	    {"comp-num-users", ACTION_COMPUTE_NUM_USERS},
	    {"comp-list-max", ACTION_COMPUTE_LIST_MAX},
	    {"comp-num-boot", ACTION_COMPUTE_NUM_BOOT},
	    {"list-hnum", ACTION_LIST_HARMONIC_NUM},
	    {"comp-hnum", ACTION_COMP_HARMONIC_NUM},
	    {0, 0}
	};

	c = getopt_long(argc, argv, "he:n:l:b:", long_options,
			&option_index);
	if (c == -1)
	    break;

	switch (c) {
	case 'h':{
		int i;

		fprintf(stdout, "%s : possible arguments are\n\n",
			argv[0]);
		for (i = 0; long_options[i].name != 0x0; i++)
		    fprintf(stdout, "--%s\n", long_options[i].name);
		fprintf(stdout, "\npossible actions are: ");
		for (i = 0; actions[i].name != 0x0; i++)
		    fprintf(stdout, "%s ", actions[i].name);
		fprintf(stdout, "\n\n");
		exit(1);
	    }
	    break;

	case 'a':{
		int i;

		for (i = 0; actions[i].name != 0x0; i++)
		    if (strncmp(optarg, actions[i].name, strlen(optarg)) ==
			0) {
			action = actions[i].code;
			break;
		    }
		if (action == -1) {
		    fprintf(stderr, "%s: invalid argument %s\n",
			    long_options[option_index].name, optarg);
		    exit(1);
		}
	    }
	    break;

	case 1:
	    errno = 0;
	    endptr = NULL;
	    num_harm_begin = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_NUM_HARM_BEGIN;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;

	case 2:
	    errno = 0;
	    endptr = NULL;
	    num_harm_end = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_NUM_HARM_END;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;

	case 3:
	    errno = 0;
	    endptr = NULL;
	    num_harm_compute = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_NUM_HARM_COMPUTE;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;

	case 'e':
	    errno = 0;
	    endptr = NULL;
	    e_est = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_E_EST;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;

	case 'n':
	    errno = 0;
	    endptr = NULL;
	    num_users = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_NUM_USERS;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;

	case 'l':
	    errno = 0;
	    endptr = NULL;
	    list_max = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_LIST_MAX;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;

	case 'b':
	    errno = 0;
	    endptr = NULL;
	    num_boot = (double) strtod(optarg, &endptr);
	    param_ok |= PARAM_NUM_BOOT;
	    if (errno != 0) {
		fprintf(stderr, "%s: cannot convert %s: %s\n",
			long_options[option_index].name, optarg,
			strerror(errno));
		exit(1);
	    } else if (*endptr != '\0') {
		fprintf(stderr, "%s: invalid argument %s\n",
			long_options[option_index].name, optarg);
		exit(1);
	    }
	    break;
	}
    }

    switch (action) {
    case ACTION_LIST_HARMONIC_NUM:
	if ((param_ok & PARAM_NUM_HARM_BEGIN) == 0x0) {
	    fprintf(stderr, "option --hnum-begin [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_NUM_HARM_END) == 0x0) {
	    fprintf(stderr, "option --hnum-end [num] missing\n");
	    exit(1);
	}
	compute_harmonic_num_list(num_harm_begin, num_harm_end);
	break;

    case ACTION_COMP_HARMONIC_NUM:
	if ((param_ok & PARAM_NUM_HARM_COMPUTE) == 0x0) {
	    fprintf(stderr, "option --hnum [num] missing\n");
	    exit(1);
	}
	compute_harmonic_num(num_harm_compute, 1);
	break;

    case ACTION_COMPUTE_E_EST:
	if ((param_ok & PARAM_NUM_USERS) == 0x0) {
	    fprintf(stderr, "option --num-users [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_LIST_MAX) == 0x0) {
	    fprintf(stderr, "option --list-max [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_NUM_BOOT) == 0x0) {
	    fprintf(stderr, "option --num-boot [num] missing\n");
	    exit(1);
	}
	compute_e_est(num_users, list_max, num_boot);
	break;

    case ACTION_COMPUTE_NUM_USERS:
	if ((param_ok & PARAM_E_EST) == 0x0) {
	    fprintf(stderr, "option --e-est [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_LIST_MAX) == 0x0) {
	    fprintf(stderr, "option --list-max [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_NUM_BOOT) == 0x0) {
	    fprintf(stderr, "option --num-boot [num] missing\n");
	    exit(1);
	}
	compute_num_users(e_est, list_max, num_boot);
	break;

    case ACTION_COMPUTE_LIST_MAX:
	if ((param_ok & PARAM_E_EST) == 0x0) {
	    fprintf(stderr, "option --e-est [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_NUM_USERS) == 0x0) {
	    fprintf(stderr, "option --num-users [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_NUM_BOOT) == 0x0) {
	    fprintf(stderr, "option --num-boot [num] missing\n");
	    exit(1);
	}
	compute_list_max(e_est, num_users, num_boot);
	break;

    case ACTION_COMPUTE_NUM_BOOT:
	if ((param_ok & PARAM_E_EST) == 0x0) {
	    fprintf(stderr, "option --e-est [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_NUM_USERS) == 0x0) {
	    fprintf(stderr, "option --num-users [num] missing\n");
	    exit(1);
	}
	if ((param_ok & PARAM_LIST_MAX) == 0x0) {
	    fprintf(stderr, "option --list-max [num] missing\n");
	    exit(1);
	}
	compute_num_boot(e_est, num_users, list_max);
	break;

    }
    return 0;
}
