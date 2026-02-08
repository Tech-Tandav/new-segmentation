# STEP 1: Start with the BASE KITCHEN
FROM python:3.11-slim
# Meaning: Get a clean room with Python 3.11 pre-installed.

# STEP 2: Install SPECIAL EQUIPMENT (Chrome)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*
# Meaning: Buy the oven (Chromium) and the gas line (Driver) needed for scraping.

# STEP 3: Set the WORK TABLE
WORKDIR /app
# Meaning: Move all operations to the /app counter.

# STEP 4: Copy the INGREDIENT LIST
COPY requirements.txt .
# Meaning: Bring the list of spices/tools needed.

# STEP 5: PREPARE INGREDIENTS
RUN pip install --no-cache-dir -r requirements.txt
# Meaning: Install all Python libraries.

# STEP 6: Bring in the RECIPE STEPS
COPY . .
# Meaning: Copy all your project code onto the counter.

# STEP 7: SET HINTS for the Chef
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
# Meaning: Tell the chef exactly where the oven and gas line are located.

# STEP 8: OPEN THE SERVICE WINDOW
EXPOSE 8000
# Meaning: Prepare to serve the app on port 8000.

# STEP 9: START COOKING
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Meaning: The default way to start the kitchen.