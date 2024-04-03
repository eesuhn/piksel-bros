def build_test() -> bool:
	from app.game import Game

	game = Game()
	test_get_sprites()
	# game.run()
	game.end()
	return True


def test_get_sprites() -> None:
	from app.utils import get_sprites

	sprites = get_sprites(["enemies", "angrypig"], 36, 30)
	# sprites = get_sprites(["terrain"], 32, 32)
	for sprite in sprites:
		# print(sprite, sprites[sprite])
		print(sprite)
