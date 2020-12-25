import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor.js';
// import InlineEditor from '@ckeditor/ckeditor5-editor-inline/src/inlineeditor.js';
import Alignment from '@ckeditor/ckeditor5-alignment/src/alignment';
import Autoformat from '@ckeditor/ckeditor5-autoformat/src/autoformat.js';
import Autosave from '@ckeditor/ckeditor5-autosave/src/autosave';
import BlockQuote from '@ckeditor/ckeditor5-block-quote/src/blockquote.js';
import Bold from '@ckeditor/ckeditor5-basic-styles/src/bold.js';
import Code from '@ckeditor/ckeditor5-basic-styles/src/code.js';
import CodeBlock from '@ckeditor/ckeditor5-code-block/src/codeblock.js';
import Essentials from '@ckeditor/ckeditor5-essentials/src/essentials.js';
import ExportToPDF from '@ckeditor/ckeditor5-export-pdf/src/exportpdf.js';
import FontBackgroundColor from '@ckeditor/ckeditor5-font/src/fontbackgroundcolor.js';
import FontColor from '@ckeditor/ckeditor5-font/src/fontcolor.js';
import FontFamily from '@ckeditor/ckeditor5-font/src/fontfamily.js';
import FontSize from '@ckeditor/ckeditor5-font/src/fontsize.js';
import Heading from '@ckeditor/ckeditor5-heading/src/heading.js';
import Highlight from '@ckeditor/ckeditor5-highlight/src/highlight.js';
import HorizontalLine from '@ckeditor/ckeditor5-horizontal-line/src/horizontalline.js';
import Image from '@ckeditor/ckeditor5-image/src/image.js';
import ImageCaption from '@ckeditor/ckeditor5-image/src/imagecaption.js';
import ImageStyle from '@ckeditor/ckeditor5-image/src/imagestyle.js';
import ImageToolbar from '@ckeditor/ckeditor5-image/src/imagetoolbar.js';
import ImageUpload from '@ckeditor/ckeditor5-image/src/imageupload.js';
import Indent from '@ckeditor/ckeditor5-indent/src/indent.js';
import IndentBlock from '@ckeditor/ckeditor5-indent/src/indentblock';
import Italic from '@ckeditor/ckeditor5-basic-styles/src/italic.js';
import Link from '@ckeditor/ckeditor5-link/src/link.js';
import List from '@ckeditor/ckeditor5-list/src/list.js';
import MediaEmbed from '@ckeditor/ckeditor5-media-embed/src/mediaembed.js';
import Paragraph from '@ckeditor/ckeditor5-paragraph/src/paragraph.js';
import PasteFromOffice from '@ckeditor/ckeditor5-paste-from-office/src/pastefromoffice';
import Table from '@ckeditor/ckeditor5-table/src/table.js';
import TableCellProperties from '@ckeditor/ckeditor5-table/src/tablecellproperties';
import TableProperties from '@ckeditor/ckeditor5-table/src/tableproperties';
import TableToolbar from '@ckeditor/ckeditor5-table/src/tabletoolbar.js';
import TextTransformation from '@ckeditor/ckeditor5-typing/src/texttransformation.js';
import Underline from '@ckeditor/ckeditor5-basic-styles/src/underline.js';
import ImageResize from "@ckeditor/ckeditor5-image/src/imageresize.js";
import SimpleUploadAdapter from '@ckeditor/ckeditor5-upload/src/adapters/simpleuploadadapter.js';

class Editor extends ClassicEditor {
}

// Plugins to include in the build.
Editor.builtinPlugins = [
  Autosave,
  Alignment,
  Autoformat,
  BlockQuote,
  Bold,
  SimpleUploadAdapter,
  Code,
  CodeBlock,
  Essentials,
  ExportToPDF,
  FontBackgroundColor,
  FontColor,
  FontFamily,
  FontSize,
  Heading,
  Highlight,
  HorizontalLine,
  Image,
  ImageCaption,
  ImageStyle,
  ImageToolbar,
  ImageUpload,
  ImageResize,
  Indent,
  IndentBlock,
  Italic,
  Link,
  List,
  MediaEmbed,
  Paragraph,
  PasteFromOffice,
  Table,
  TableCellProperties,
  TableProperties,
  TableToolbar,
  TextTransformation,
  Underline,
];

Editor.defaultConfig = {
  toolbar: {
    items: [
      // 'CKFinder',
      'undo', 'redo',
      '|', 'heading',
      '|', 'bold', 'italic', 'underline', 'highlight',
      '|', 'imageUpload', 'link', 'bulletedList', 'numberedList',
      '|', 'indent', 'outdent',
      '|', 'blockQuote', 'insertTable', 'mediaEmbed',
      // '|', 'alignment', 'fontFamily', 'fontSize',
      '|', 'fontColor', 'fontBackgroundColor',
      '|', 'exportPdf', /*'codeBlock', 'code', */ 'horizontalLine',
    ]
  },
  image: {
    toolbar: [
      'imageStyle:full', 'imageStyle:side',
      '|', 'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight',
      '|', 'imageTextAlternative',
    ],
    styles: [
      'full',
      "side",
      'alignLeft',
      'alignCenter',
      'alignRight',
    ]
  },
  table: {
    contentToolbar: [
      'tableColumn', 'tableRow', 'mergeTableCells',
      '|', 'tableCellProperties', 'tableProperties'
    ]
  },

  simpleUpload: {
    uploadUrl: "/admin/ckeditor/upload_photo/news/media"
  },

  autosave: {
    save(editor) {
      editor.updateSourceElement();
      return editor;
    }
  },

  language: 'ru',

};

export default Editor;
