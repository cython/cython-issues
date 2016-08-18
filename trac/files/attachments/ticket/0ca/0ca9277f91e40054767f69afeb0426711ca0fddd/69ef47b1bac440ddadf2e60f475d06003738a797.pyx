# HG changeset patch
# User Jason Evans <jasone@canonware.com>
# Date 1229734247 28800
# Node ID 3569aa5167f1c2440e0eeb39406cc6ad84cdf741
# Parent  965dc9fc3da792af6edebf5ecaa1df376a1d1290
Set module name for Spam/__init__.pyx to Spam.

diff --git a/Cython/Compiler/Symtab.py b/Cython/Compiler/Symtab.py
--- a/Cython/Compiler/Symtab.py
+++ b/Cython/Compiler/Symtab.py
@@ -805,7 +805,12 @@
         self.parent_module = parent_module
         outer_scope = context.find_submodule("__builtin__")
         Scope.__init__(self, name, outer_scope, parent_module)
-        self.module_name = name
+        if name != "__init__":
+            self.module_name = name
+        else:
+            # Treat Spam/__init__.pyx specially, so that when Python loads
+            # Spam/__init__.so, initSpam() is defined.
+            self.module_name = parent_module.module_name
         self.context = context
         self.module_cname = Naming.module_cname
         self.module_dict_cname = Naming.moddict_cname
