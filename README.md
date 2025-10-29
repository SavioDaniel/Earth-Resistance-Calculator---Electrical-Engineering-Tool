⚡ Earth Resistance Calculator
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/GUI-Tkinter-green
https://img.shields.io/badge/License-MIT-yellow
https://img.shields.io/badge/Field-Electrical%2520Engineering-orange

A comprehensive tool for calculating electrical grounding resistance developed in Python with an intuitive graphical interface.

🎯 About the Project
This calculator enables the design of grounding systems through four different configurations, meeting the needs of electrical projects and lightning protection systems (LPS).

✨ Features
🔧 Supported Configurations
📍 Single Vertical Rod

Calculation for single vertical electrodes

Formula: R = ρ/(2πL) × [ln(4L/d) - 1]

📏 Multiple Rods in Line

System with multiple aligned rods

Considers mutual effect between rods

Formula: R = ρ/(2πnL) × [ln(4L/d) - 1 + 2(L/s)ln(2n/π)]

➖ Buried Horizontal Conductor

Underground horizontal electrodes

Applied Dwight's formula

Formula: R = ρ/(2πL) × [ln(2L/d) + ln(L/2h) - 2 + 2h/L]

🔲 Grounding Grid

Mesh systems for substations

Simplified formula for rectangular grids

Formula: R = ρ × (1/L + 1/√(20A)) × (1 + 1/(1 + h√(A/10)))

🚀 How to Use
Prerequisites
Python 3.8 or higher

Libraries: tkinter (included in standard Python installation)

Installation
bash
# Clone the repository
git clone https://github.com/your-username/earth-resistance-calculator.git

# Enter the directory
cd earth-resistance-calculator

# Run the application
python grounding_calculator.py
Execution
Run the Python script

Select the desired electrode type

Enter soil resistivity

Fill in configuration-specific data

Click "Calculate Resistance"

📊 Usage Examples
Single Rod Calculation
python
Soil resistivity: 100 Ω.m
Rod length: 3.0 m
Rod diameter: 0.016 m
Result: 35.12 Ω
Grid Calculation
python
Soil resistivity: 100 Ω.m
Grid area: 36 m²
Total conductor length: 24 m
Depth: 0.5 m
Result: 11.94 Ω
🧪 Calculation Validation
All calculations have been manually validated and follow established electrical engineering formulas:

Single rod: Modified Dwight's formula

Multiple rods: Schwarz's formula for aligned rods

Horizontal conductor: Complete Dwight's formula

Grid: Simplified formula for rectangular grids

📈 Results Analysis
The system includes automatic analysis according to technical standards:

✅ Excellent: ≤ 1Ω (Sensitive systems)

✅ Very Good: ≤ 5Ω (Telecommunications)

✅ Good: ≤ 10Ω (Power systems)

❌ Needs improvement: > 10Ω

🛠️ Technologies Used
Language: Python 3.8+

Graphical Interface: Tkinter

Mathematics: Math library

Validation: Exception handling

📁 Project Structure
text
earth-resistance-calculator/
│
├── grounding_calculator.py
├── README.md
├── requirements.txt
├── LICENSE
└── examples/
    └── usage_examples.md
👨‍💻 Development
To contribute:
Fork the project

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🎓 Applications
Building and industrial electrical projects

Lightning protection systems (LPS)

Electrical substations

Telecommunications

Testing laboratories

⚠️ Disclaimer
This tool is for preliminary design only. Final validation must be performed through on-site measurements by qualified professionals.

🔬 Testing Data
The calculator has been tested with the following reference values:

Configuration	Parameters	Expected Result
Single Rod	ρ=100Ω.m, L=3.0m, d=0.016m	35.12 Ω
Multiple Rods	ρ=100Ω.m, n=3, L=2.4m, d=0.016m, s=2.4m	14.79 Ω
Horizontal Conductor	ρ=100Ω.m, L=15m, d=0.010m, h=0.6m	9.14 Ω
Grounding Grid	ρ=100Ω.m, A=36m², L=24m, h=0.5m	11.94 Ω
📞 Contact
Your Name - @SavioDaniel

Project Link: https://github.com/SavioDaniel/Earth-Resistance-Calculator---Electrical-Engineering-Tool

⭐️ If this project was useful, please give it a star!
