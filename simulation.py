from helpers import *

MAX_BANDWIDTH = 100000  # Maximum bandwidth is 100Gbps


def static_beta_assignment_test():
    ab_values = [[1, 0.5], [1, 0.6], [1, 0.7], [1, 0.8], [1, 0.9]]
    latencies = []
    latencies_std = []
    throughputs = []
    throughputs_std = []
    for a, b in ab_values:
        tcp_reno1 = TCPReno(
            a,
            b,
            initial_cwnd=25,
            max_cwnd=100,
            bandwidth=5000,
            rtt=0.001,
            max_bandwidth=MAX_BANDWIDTH,
            name="TCP Reno 1",
        )
        tcp_reno2 = TCPReno(
            a,
            b,
            initial_cwnd=75,
            max_cwnd=100,
            bandwidth=5000,
            rtt=0.001,
            max_bandwidth=MAX_BANDWIDTH,
            name="TCP Reno 2",
        )

        simulate_shared_environment(tcp_reno1, tcp_reno2, max_iters=1000)

        # plot_reno(tcp_reno1, tcp_reno2)

        # Print metrics
        print("Alpha:", a, "Beta:", b)
        # tcp_reno1.print_metrics()
        # tcp_reno2.print_metrics()
        latency1, latency_std1, throughput1, throughput_std1, bdp1 = (
            tcp_reno1.get_metrics()
        )
        # latencies.append(latency1)
        # latencies_std.append(latency_std1)
        # throughputs.append(throughput1)
        # throughputs_std.append(throughput_std1)

        latency2, latency_std2, throughput2, throughput_std2, bdp2 = (
            tcp_reno2.get_metrics()
        )
        latencies.append((latency1 + latency2) / 2)
        latencies_std.append((latency_std1 + latency_std2) / 2)
        throughputs.append((throughput1 + throughput2) / 2)
        throughputs_std.append((throughput_std1 + throughput_std2) / 2)

        # Plot metrics
        # plot_comparison_metrics(tcp_reno1, tcp_reno2)

    print("Latencies:", latencies)
    print("Latencies Std:", latencies_std)
    print("Throughputs:", throughputs)
    print("Throughputs Std:", throughputs_std)

    x = [0.5, 0.6, 0.7, 0.8, 0.9]
    # plt.figure(figsize=(12, 6))
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("TCP Reno Latency Over Beta")
    axes[0].set_xlabel("Beta")
    axes[0].set_ylabel("Latency (seconds)")
    axes[0].errorbar(x, latencies, yerr=latencies_std, fmt="o-", label="Latency")
    # axes[1].subplot(1, 2, 2)
    axes[1].set_title("TCP Reno Throughput Over Beta")
    axes[1].set_xlabel("Beta")
    axes[1].set_ylabel("Throughput (KB/s)")
    axes[1].errorbar(x, throughputs, yerr=throughputs_std, fmt="o-", label="Throughput")
    plt.tight_layout()
    plt.show()


def static_alpha_assignment_test():
    ab_values = [[1, 0.8], [2, 0.8], [3, 0.8], [4, 0.8], [5, 0.8], [6, 0.8]]
    latencies = []
    latencies_std = []
    throughputs = []
    throughputs_std = []
    for a, b in ab_values:
        tcp_reno1 = TCPReno(
            a,
            b,
            initial_cwnd=25,
            max_cwnd=100,
            bandwidth=5000,
            rtt=0.001,
            max_bandwidth=MAX_BANDWIDTH,
            name="TCP Reno 1",
        )
        tcp_reno2 = TCPReno(
            a,
            b,
            initial_cwnd=75,
            max_cwnd=100,
            bandwidth=5000,
            rtt=0.001,
            max_bandwidth=MAX_BANDWIDTH,
            name="TCP Reno 2",
        )

        simulate_shared_environment(tcp_reno1, tcp_reno2, max_iters=1000)

        plot_reno(tcp_reno1, tcp_reno2)

        # Print metrics
        print("Alpha:", a, "Beta:", b)
        # tcp_reno1.print_metrics()
        # tcp_reno2.print_metrics()
        latency1, latency_std1, throughput1, throughput_std1, bdp1 = (
            tcp_reno1.get_metrics()
        )
        # latencies.append(latency1)
        # latencies_std.append(latency_std1)
        # throughputs.append(throughput1)
        # throughputs_std.append(throughput_std1)

        latency2, latency_std2, throughput2, throughput_std2, bdp2 = (
            tcp_reno2.get_metrics()
        )
        latencies.append((latency1 + latency2) / 2)
        latencies_std.append((latency_std1 + latency_std2) / 2)
        throughputs.append((throughput1 + throughput2) / 2)
        throughputs_std.append((throughput_std1 + throughput_std2) / 2)

        # Plot metrics
        # plot_comparison_metrics(tcp_reno1, tcp_reno2)

    print("Latencies:", latencies)
    print("Latencies Std:", latencies_std)
    print("Throughputs:", throughputs)
    print("Throughputs Std:", throughputs_std)

    x = [1, 2, 3, 4, 5, 6]
    # plt.figure(figsize=(12, 6))
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("TCP Reno Latency Over Alpha")
    axes[0].set_xlabel("Alpha")
    axes[0].set_ylabel("Latency (seconds)")
    axes[0].errorbar(x, latencies, yerr=latencies_std, fmt="o-", label="Latency")
    # axes[1].subplot(1, 2, 2)
    axes[1].set_title("TCP Reno Throughput Over Alpha")
    axes[1].set_xlabel("Alpha")
    axes[1].set_ylabel("Throughput (KB/s)")
    axes[1].errorbar(x, throughputs, yerr=throughputs_std, fmt="o-", label="Throughput")
    plt.tight_layout()
    plt.show()


static_alpha_assignment_test()
