import numpy as np
import matplotlib.pyplot as plt


class TCPReno:
    def __init__(
        self,
        alpha,
        beta,
        initial_cwnd=1,
        max_cwnd=10,
        rtt=1,  # Default RTT set to 1 second for simplicity
        bandwidth=10,  # Bandwidth in Mbps
        max_bandwidth=100,  # Maximum bandwidth in Mbps
        alpha_update_fn=lambda a: a,
        beta_update_fn=lambda b: b,
        name="TCP Reno",
    ) -> None:
        self.name = name
        self.alpha = alpha
        self.beta = beta
        self.cwnd = initial_cwnd
        self.max_cwnd = max_cwnd
        self.rtt = rtt
        self.bandwidth = bandwidth
        self.max_bandwidth = max_bandwidth
        self.bdp = self.bandwidth * self.rtt * (10**6 / 8)  # BDP in bytes

        self.cwnd_vals = []
        self.latency_vals = []  # To store latency values
        self.throughput_vals = []  # To store throughput values

        self.alpha_increase_fn = alpha_update_fn
        self.beta_decrease_fn = beta_update_fn

    def additive_increase(self):
        self.cwnd = min(self.cwnd + self.alpha, self.max_cwnd)
        self.alpha = self.alpha_increase_fn(self.alpha)
        self.alpha = min(8, self.alpha + 1)
        self.beta = min(0.9, self.beta + 0.1)

    def multiplicative_decrease(self):
        self.cwnd = max(int(self.cwnd * self.beta), 1)
        self.beta = self.beta_decrease_fn(self.beta)
        self.alpha = max(1, self.alpha - 1)
        self.beta = max(0.5, self.beta - 0.1)

    def update_latency(self):
        packet_size = 1  # in KB
        data_in_flight = self.cwnd * packet_size  # in KB
        bandwidth_kb = self.bandwidth * 1000 / 8  # Convert bandwidth from Mbps to KBps
        transmission_delay = data_in_flight / bandwidth_kb  # in seconds
        self.latency = self.rtt + transmission_delay  # Total latency
        self.latency_vals.append(self.latency)
        # self.latency_vals.append(self.cwnd / self.bandwidth)

    def update_throughput(self, time_step=1):
        # Assuming each cwnd unit corresponds to 1 packet of a fixed size, e.g., 1KB
        packet_size_kb = 1  # in KB
        data_transmitted_kb = self.cwnd * packet_size_kb  # in KB
        throughput_kb_s = data_transmitted_kb / time_step  # in KB/s
        self.throughput_vals.append(
            throughput_kb_s
        )  # Store throughput for this iteration

    def check_bandwidth(self):
        # Check if current bandwidth exceeds max bandwidth and adjust if necessary
        packet_size = 1  # in KB
        data_in_flight = self.cwnd * packet_size  # in KB
        required_bandwidth = data_in_flight / self.rtt  # Required bandwidth in KBps
        required_bandwidth_mbps = required_bandwidth * 8 / 1000  # Convert to Mbps
        if required_bandwidth_mbps > self.max_bandwidth:
            self.bandwidth = self.max_bandwidth
        else:
            self.bandwidth = required_bandwidth_mbps

    def get_metrics(self):
        latency = np.mean(self.latency_vals)
        latency_std = np.std(self.latency_vals)
        throughput = np.mean(self.throughput_vals)
        throughput_std = np.std(self.throughput_vals)
        bdp = self.bdp
        return latency, latency_std, throughput, throughput_std, bdp

    def print_metrics(self):
        print("Metrics for", self.name)
        print(f"Average Latency: {np.mean(self.latency_vals) * 1000:.2f} msec")
        print(
            f"Standard Deviation of Latency: {np.std(self.latency_vals) * 1000:.2f} msec"
        )
        print(f"Average Throughput: {np.mean(self.throughput_vals):.2f} KB/s")
        print(
            f"Standard Deviation of Throughput: {np.std(self.throughput_vals):.2f} KB/s"
        )
        print(f"Bandwidth-Delay Product: {self.bdp:.2f} bytes")

    def plot_metrics(self):
        # Plotting Latency and Throughput for tcp_reno1 as an example
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(self.latency_vals, "o-", label="Latency")
        plt.xlabel("Iteration")
        plt.ylabel("Latency (seconds)")
        plt.title("TCP Reno Latency Over Time for " + self.name)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.throughput_vals, "o-", label="Throughput")
        plt.xlabel("Iteration")
        plt.ylabel("Throughput (KB/s)")
        plt.title("TCP Reno Throughput Over Time for " + self.name)
        plt.legend()

        plt.tight_layout()
        plt.show()


def simulate_shared_environment(tcp_reno1, tcp_reno2, max_iters=100):
    total_data_sent = 0
    for _ in range(max_iters):
        tcp_reno1.cwnd_vals.append(tcp_reno1.cwnd)
        tcp_reno2.cwnd_vals.append(tcp_reno2.cwnd)

        total_data_sent += tcp_reno1.cwnd

        if (tcp_reno1.cwnd + tcp_reno2.cwnd) < tcp_reno1.max_cwnd:
            tcp_reno1.additive_increase()
            tcp_reno2.additive_increase()
        else:
            tcp_reno1.multiplicative_decrease()
            tcp_reno2.multiplicative_decrease()

        tcp_reno1.update_latency()
        tcp_reno2.update_latency()

        tcp_reno1.update_throughput()
        tcp_reno2.update_throughput()

        tcp_reno1.check_bandwidth()
        tcp_reno2.check_bandwidth()


def plot_reno(tcp_reno1, tcp_reno2):
    plt.plot(tcp_reno1.cwnd_vals, tcp_reno2.cwnd_vals, "o-", label="TCP Reno Instances")
    plt.plot(
        [0, tcp_reno1.max_cwnd], [tcp_reno1.max_cwnd, 0], "r--", label="Efficiency Line"
    )
    plt.plot(
        [0, tcp_reno1.max_cwnd], [0, tcp_reno1.max_cwnd], "g--", label="Fairness Line"
    )

    start_x, start_y = tcp_reno1.cwnd_vals[0], tcp_reno2.cwnd_vals[0]
    end_x, end_y = tcp_reno1.cwnd_vals[-1], tcp_reno2.cwnd_vals[-1]
    plt.text(
        start_x, start_y, "Start", horizontalalignment="right", verticalalignment="top"
    )
    plt.text(
        end_x, end_y, "End", horizontalalignment="left", verticalalignment="bottom"
    )

    plt.xlabel("TCP Reno 1 cwnd")
    plt.ylabel("TCP Reno 2 cwnd")
    plt.title("TCP Reno AIMD Simulation in Shared Environment")
    plt.legend()
    plt.show()


def plot_comparison_metrics(obj1, obj2):
    plt.figure(figsize=(12, 6))

    # Latency Comparison
    plt.subplot(1, 2, 1)
    plt.plot(obj1.latency_vals, "o-", label=f"Latency {obj1.name}")
    plt.plot(obj2.latency_vals, "s--", label=f"Latency {obj2.name}")
    plt.xlabel("Iteration")
    plt.ylabel("Latency (seconds)")
    plt.title("TCP Reno Latency Over Time")
    plt.legend()

    # Throughput Comparison
    plt.subplot(1, 2, 2)
    plt.plot(obj1.throughput_vals, "o-", label=f"Throughput {obj1.name}")
    plt.plot(obj2.throughput_vals, "s--", label=f"Throughput {obj2.name}")
    plt.xlabel("Iteration")
    plt.ylabel("Throughput (KB/s)")
    plt.title("TCP Reno Throughput Over Time")
    plt.legend()

    plt.tight_layout()
    plt.show()
