from cx_Freeze import setup, Executable

setup(
	name = "Projet Galax Example",
	version = "0.1",
	description = "Galax",
	executables = [Executable("galax_5.py")],
)