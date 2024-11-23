# SysMon

SysMon is a system monitoring application that tracks CPU, memory, disk, network, and GPU usage thresholds. It provides an interface for setting and retrieving these thresholds and supports theme customization. Project for COMP-7082.

## Features

- Monitor CPU, memory, disk, network, and GPU usage
- Set thresholds for system metrics
- Customizable theme settings
- Uses FastAPI for the backend and MySQL for the database
- Dockerized for easy setup

## Prerequisites

- Python 3.8+
- Docker
- Docker Compose

## Installation

### Local Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/towelie03/SysMon.git
   cd SysMon

   docker-compose up --build
   ```


























### old readme

For Server:
    Create/ Slash start the virtual environment

    Install the Requirements:
        pip install -r requirements.txt
        run: uvicorn server:app --reload

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```
