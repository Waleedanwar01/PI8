function initTinyMCEEditors() {
  if (typeof tinymce === "undefined") {
    if (typeof window.__tinymceInitTries === "undefined") {
      window.__tinymceInitTries = 0;
    }
    if (window.__tinymceInitTries >= 20) {
      return;
    }
    window.__tinymceInitTries += 1;
    setTimeout(initTinyMCEEditors, 300);
    return;
  }

  // Clear any previous instances (useful on admin inlines / navigations)
  tinymce.remove();

  tinymce.init({
    selector: "textarea.tinymce-editor",
    height: 400,
    menubar: true,
    plugins:
      "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table help wordcount",
    toolbar:
      "undo redo | formatselect | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | removeformat | code | fullscreen",
    images_upload_url: '/upload-image/', 
    automatic_uploads: true,
    file_picker_types: 'image',
    content_style:
      "body { font-family: -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif; font-size:14px } img { max-width: 100%; height: auto; }",
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initTinyMCEEditors);
} else {
  initTinyMCEEditors();
}
