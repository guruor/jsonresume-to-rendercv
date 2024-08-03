# JSONResume to RenderCV Converter 🚀

Convert your resume from the JSON Resume schema to the RenderCV schema effortlessly with this CLI tool.

## Features ✨

- Converts JSON Resume schema to RenderCV schema.
- Validates input and output against their respective schemas.
- Supports both JSON and YAML formats for input and output.

## Installation 📦

You can install the tool using `pip`:

```sh
pip install jsonresume_to_rendercv
```

## Usage 📝

Convert your resume from JSON Resume to RenderCV schema using the command-line interface.

### Example Usage

#### JSON Input

```sh
jsonresume_to_rendercv resume.json output.yaml
```

#### YAML Input

```sh
jsonresume_to_rendercv resume.yaml output.yaml
```

## Development 🛠️

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/jsonresume_to_rendercv.git
   cd jsonresume_to_rendercv
   ```

2. **Install dependencies:**

   ```sh
   make install
   ```

### Building the Project

To build the project:

```sh
make build
```

### Running Tests

To run tests:

```sh
make test
```

This will download a sample JSON Resume file, run the converter, and validate the output.

### Releasing the Package

To release the package:

```sh
make release
```

## Contributing 🤝

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙌

- [JSON Resume Schema](https://github.com/jsonresume/resume-schema)
- [RenderCV Schema](https://github.com/sinaatalay/rendercv)
