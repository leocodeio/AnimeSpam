# Contributing to AnimeSpam

Thank you for your interest in contributing to AnimeSpam! This document provides guidelines for contributing to the project.

## Project Structure

AnimeSpam consists of multiple codebases:
- `animespam/` - The main website (React/Vite frontend)
- `anime_upscaler_v1/` - Legacy upscaler implementation
- `anime_upscaler_v2/` - Current upscaler implementation (if available)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python 3.8+ (for upscaler components)
- Git

### Setting up the development environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/AnimeSpam.git
   cd AnimeSpam
   ```

3. For the website development:
   ```bash
   cd animespam
   npm install
   npm run dev
   ```

4. For upscaler development:
   ```bash
   cd anime_upscaler_v1
   pip install -r requirements.txt
   ```

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide system information when relevant
- For upscaling issues, include sample images/videos when possible

### Submitting Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards
3. Test your changes thoroughly
4. Commit with clear, descriptive messages:
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

4. Push to your fork and submit a pull request

### Pull Request Guidelines

- Include a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep commits focused and atomic

## Coding Standards

### Frontend (animespam/)
- Use ESLint configuration provided
- Follow React best practices
- Use Tailwind CSS for styling
- Maintain responsive design

### Backend/Upscaler
- Follow PEP 8 for Python code
- Include docstrings for functions
- Handle errors gracefully
- Optimize for performance

## Development Workflow

1. Check existing issues before starting work
2. Discuss major changes in issues first
3. Write tests for new functionality
4. Update documentation as needed
5. Ensure code passes all checks

## Testing

### Frontend
```bash
cd animespam
npm run test
npm run lint
```

### Upscaler
```bash
cd anime_upscaler_v1
python -m pytest tests/
```

## Performance Considerations

- Optimize image/video processing algorithms
- Consider memory usage for large files
- Test with various input formats
- Profile critical code paths

## Documentation

- Update README.md for significant changes
- Include JSDoc comments for JavaScript functions
- Document API endpoints and parameters
- Provide usage examples

## Community Guidelines

- Be respectful and inclusive
- Help newcomers get started
- Provide constructive feedback
- Follow the code of conduct

## Questions?

- Open an issue for technical questions
- Join discussions in existing issues
- Check documentation first

Thank you for contributing to AnimeSpam!