from app import App


def main() -> None:
	app = App.select_app()
	app.run()


if __name__ == "__main__":
	main()
