-----------------------
Working with projects 
-----------------------

- Saving the current RepTate session to a project file
- Opening an existing RepTate project file
- Sharing projects with collaborators

A RepTate project stores the current analysis session in a ``.rept`` file.
Use the ``Save RepTate Project`` button in the project toolbar to save the
session, and use ``Open RepTate Project`` to load a saved project. Both actions
open a file dialog for files with the ``.rept`` extension.

A saved project contains the open applications, their datasets, loaded data
tables, file parameters, active/inactive file state, theories, theory
parameters, stored theory tables, tools, tool parameters, annotations, selected
views, dataset plotting settings, axis options, and legend options. The project
file is a compressed file that contains a JSON description of the session.

When a project is opened, RepTate first reads the project file and reports how
many applications, theories, files, and tools will be loaded. If the user
confirms, RepTate recreates the applications, datasets, files, theories, tools,
annotations, selected views, and visible data-inspector state. Project files
can also be opened at startup when a ``.rept`` file is passed to RepTate.

Projects are useful for returning to an analysis later or sharing a complete
RepTate session with a collaborator. Because the data tables and theory results
are stored in the project, collaborators do not need the original data files in
the same folder to reopen the saved session. They do need a compatible RepTate
version and the same application/theory support used by the project.

If a project file is corrupted or does not contain the expected project data,
RepTate does not load it and reports the problem in the console. Saving a
project records the state at that moment; changes made later are not included
until the project is saved again.
