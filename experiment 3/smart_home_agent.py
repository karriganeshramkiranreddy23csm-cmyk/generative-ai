import time
import random
import os
import sys
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime

class SmartHomeEnvironment:
    """
    Simulates the environment (the room).
    Maintains the current room temperature and outside temperature.
    Simulates natural temperature changes and the cooling effect of the AC.
    """
    def __init__(self, initial_temp=25.0, outside_temp=31.2):
        self.room_temp = initial_temp
        self.outside_temp = outside_temp
        self.ac_is_on = False

    def update(self):
        """
        Updates the room temperature based on natural warming and AC cooling.
        This simulates physics.
        """
        # Natural warming from outside (slow increase)
        natural_warming_rate = random.uniform(0.05, 0.15)
        
        # Cooling from AC (fast decrease)
        ac_cooling_rate = random.uniform(0.3, 0.5)

        if self.ac_is_on:
            self.room_temp -= ac_cooling_rate
        else:
            # Only warm up if room is cooler than outside
            if self.room_temp < self.outside_temp:
                self.room_temp += natural_warming_rate

        # Add a tiny bit of random noise for realism
        self.room_temp += random.uniform(-0.02, 0.02)

    def set_ac_status(self, status):
        """Allows the agent to execute an action on the environment."""
        self.ac_is_on = status

    def get_sensor_reading(self):
        """Provides the current percept to the agent."""
        return self.room_temp


class TemperatureControlAgent:
    """
    Goal-Based Intelligent Agent.
    Goal: Maintain temperature between 22Â deg C and 24Â deg C.
    """
    def __init__(self, min_temp=22.0, max_temp=24.0):
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.ac_status = False
        self.last_reasoning = ""

    def evaluate_state_and_decide(self, current_temp):
        """
        The decision-making logic of the agent.
        Takes the percept (current_temp), compares it to the goal, and decides on an action.
        """
        if current_temp > self.max_temp:
            if not self.ac_status:
                self.last_reasoning = f"Temperature {current_temp:.1f}Â deg C â†’ Above comfort range ({self.max_temp}Â deg C) â†’ AC turned ON"
            else:
                self.last_reasoning = f"Temperature {current_temp:.1f}Â deg C â†’ Above comfort range ({self.max_temp}Â deg C) â†’ AC remains ON (COOLING)"
            self.ac_status = True
        elif current_temp < self.min_temp:
            if self.ac_status:
                self.last_reasoning = f"Temperature {current_temp:.1f}Â deg C â†’ Below comfort range ({self.min_temp}Â deg C) â†’ AC turned OFF"
            else:
                self.last_reasoning = f"Temperature {current_temp:.1f}Â deg C â†’ Comfortable / Cool â†’ AC remains OFF"
            self.ac_status = False
        else:
            # Within the hysteresis band
            self.last_reasoning = f"Temperature {current_temp:.1f}Â deg C â†’ Within comfort range â†’ AC maintains previous state ({'ON' if self.ac_status else 'OFF'})"
            # Maintain previous state

        return self.ac_status


class Simulation:
    """
    Manages the simulation loop, dashboard, and graph updates.
    """
    def __init__(self, duration_seconds=60):
        self.duration_seconds = duration_seconds
        self.env = SmartHomeEnvironment(initial_temp=26.0)
        self.agent = TemperatureControlAgent()
        
        # Data tracking for graph and summary
        self.history_time = []
        self.history_temp = []
        self.history_ac = []
        
        # Statistics
        self.initial_temp = self.env.get_sensor_reading()
        self.total_ac_on_time = 0
        self.ac_state_changes = 0
        self.exceeded_count = 0
        self.last_ac_state = False

    def clear_terminal(self):
        """Clears the terminal for a clean dashboard update."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def setup_plot(self):
        """Initializes the matplotlib live graph with a light premium theme."""
        plt.ion()
        # Premium Light Theme Colors
        # Background: very soft cream/off-white #FAF9F6
        # Graph Line: elegant deep blue #1D3557 or soft teal #457B9D
        # Target area: pale gold/champagne #F1FAEE
        
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.fig.patch.set_facecolor('#FAF9F6')
        self.ax.set_facecolor('#FAF9F6')
        
        self.line, = self.ax.plot([], [], color='#1D3557', linewidth=2.5, label='Room Temp')
        
        # Comfort Range
        self.ax.axhspan(self.agent.min_temp, self.agent.max_temp, facecolor='#457B9D', alpha=0.15, label='Comfort Range (22-24Â deg C)')
        self.ax.axhline(23.0, color='#E63946', linestyle='--', linewidth=1, alpha=0.6, label='Target (23Â deg C)')
        
        self.ax.set_title('Smart Home Temperature Control Agent (Live)', color='#1D3557', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Time (seconds)', color='#1D3557', fontsize=11)
        self.ax.set_ylabel('Temperature (Â deg C)', color='#1D3557', fontsize=11)
        self.ax.tick_params(colors='#1D3557')
        
        # AC status indicator
        self.ac_indicator = self.ax.text(0.02, 0.95, 'AC: OFF', transform=self.ax.transAxes, 
                                         fontsize=12, fontweight='bold', color='#E63946',
                                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, boxstyle='round,pad=0.5'))
        
        self.ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_color('#1D3557')
        self.ax.spines['left'].set_color('#1D3557')
        self.ax.grid(True, linestyle=':', color='#A8DADC', alpha=0.7)

    def update_plot(self, current_time):
        """Updates the matplotlib graph data."""
        self.line.set_xdata(self.history_time)
        self.line.set_ydata(self.history_temp)
        
        self.ax.set_xlim(max(0, current_time - 30), max(30, current_time + 5))
        min_y = min(20.0, min(self.history_temp) - 1) if self.history_temp else 20.0
        max_y = max(27.0, max(self.history_temp) + 1) if self.history_temp else 27.0
        self.ax.set_ylim(min_y, max_y)
        
        if self.agent.ac_status:
            self.ac_indicator.set_text('AC: ON (Cooling)')
            self.ac_indicator.set_color('#2A9D8F')
        else:
            self.ac_indicator.set_text('AC: OFF (Warming)')
            self.ac_indicator.set_color('#E63946')
            
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def display_dashboard(self, current_time):
        """Prints the real-time terminal dashboard."""
        self.clear_terminal()
        
        ac_str = "ON" if self.agent.ac_status else "OFF"
        decision_str = "COOLING" if self.agent.ac_status else "IDLE"
        temp = self.env.get_sensor_reading()
        
        dashboard = f"""
====================================================
        SMART HOME TEMPERATURE CONTROL AGENT
====================================================
Simulation Time : 00:{int(current_time):02d}
Room Temperature: {temp:.1f} Â deg C
Outside Temp    : {self.env.outside_temp:.1f} Â deg C
Target Range    : {self.agent.min_temp:.1f} - {self.agent.max_temp:.1f} Â deg C
Target Temp     : 23.0 Â deg C

AC Status       : {ac_str}
Agent Decision  : {decision_str}
Current Goal    : Maintain comfortable temperature

Agent Reasoning:
{self.agent.last_reasoning}

Agent Status    : RUNNING
====================================================
"""
        sys.stdout.write(dashboard)
        sys.stdout.flush()

    def run(self):
        """Main simulation loop."""
        self.setup_plot()
        start_time = time.time()
        
        try:
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > self.duration_seconds:
                    break
                
                # 1. Environment: Get current state (Sensors/Percepts)
                current_temp = self.env.get_sensor_reading()
                
                # Update statistics
                if current_temp > self.agent.max_temp or current_temp < self.agent.min_temp:
                    self.exceeded_count += 1
                
                # 2. Agent: Evaluate state and make a decision (Decision-Making/Actions)
                ac_command = self.agent.evaluate_state_and_decide(current_temp)
                
                # Track AC stats
                if ac_command:
                    self.total_ac_on_time += 0.5 # assuming 0.5s loop
                if ac_command != self.last_ac_state:
                    self.ac_state_changes += 1
                    self.last_ac_state = ac_command

                # 3. Environment: Apply agent action (Feedback)
                self.env.set_ac_status(ac_command)
                
                # 4. Environment: Simulate passage of time
                self.env.update()
                
                # Record history
                self.history_time.append(elapsed_time)
                self.history_temp.append(current_temp)
                self.history_ac.append(ac_command)
                
                # Update visual outputs
                self.display_dashboard(elapsed_time)
                self.update_plot(elapsed_time)
                
                # Wait for next simulation cycle
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            pass # Allow graceful exit on Ctrl+C
            
        self.display_summary()
        plt.ioff()
        plt.show() # Keep final graph open

    def display_summary(self):
        """Displays the final results of the simulation."""
        self.clear_terminal()
        
        final_temp = self.history_temp[-1] if self.history_temp else self.initial_temp
        avg_temp = sum(self.history_temp) / len(self.history_temp) if self.history_temp else self.initial_temp
        min_temp = min(self.history_temp) if self.history_temp else self.initial_temp
        max_temp = max(self.history_temp) if self.history_temp else self.initial_temp
        
        # Determine if goal was generally achieved (e.g., within range for majority of time)
        in_range_count = sum(1 for t in self.history_temp if self.agent.min_temp <= t <= self.agent.max_temp)
        success_rate = (in_range_count / len(self.history_temp)) * 100 if self.history_temp else 0
        goal_status = "ACHIEVED" if success_rate > 50 else "FAILED"
        perf_status = "SUCCESS" if success_rate > 50 else "POOR"

        summary = f"""
====================================================
              SIMULATION COMPLETE
====================================================
Initial Temperature : {self.initial_temp:.1f}Â deg C
Final Temperature   : {final_temp:.1f}Â deg C
Average Temperature : {avg_temp:.1f}Â deg C
Minimum Temperature : {min_temp:.1f}Â deg C
Maximum Temperature : {max_temp:.1f}Â deg C

Total AC ON Time    : {int(self.total_ac_on_time)} seconds
AC State Changes    : {self.ac_state_changes}

Comfort Goal        : {goal_status} ({success_rate:.1f}% time in range)
Agent Performance   : {perf_status}
====================================================
"""
        print(summary)


if __name__ == "__main__":
    print("Starting Smart Home Environment Simulation...")
    sim = Simulation(duration_seconds=60)
    sim.run()

"""
---
College Laboratory Record Conclusion:
This experiment successfully demonstrates a goal-based intelligent agent. The 
TemperatureControlAgent constantly monitors its environment via sensor percepts (room temperature), 
evaluates this input against its internal goals (22-24Â deg C), and autonomously executes actions 
(turning the AC ON/OFF). The simulation illustrates the closed-loop feedback process vital to 
intelligent systems, maintaining homeostasis within the environment through simple, transparent AI logic.
---
"""
