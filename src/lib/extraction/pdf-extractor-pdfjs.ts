import * as pdfjsLib from 'pdfjs-dist';

// Configure worker
if (typeof window === 'undefined') {
    // Server-side: use legacy build
    pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;
}

export async function extractTextFromPdfJS(buffer: Buffer): Promise<string> {
    try {
        console.log('[PDF.js Extractor] Starting extraction...');

        // Load the PDF document
        const loadingTask = pdfjsLib.getDocument({
            data: new Uint8Array(buffer),
            useSystemFonts: true,
        });

        const pdf = await loadingTask.promise;
        console.log('[PDF.js Extractor] PDF loaded, pages:', pdf.numPages);

        let fullText = '';

        // Extract text from each page
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const textContent = await page.getTextContent();

            const pageText = textContent.items
                .map((item: any) => item.str)
                .join(' ');

            fullText += pageText + '\n\n';
        }

        console.log('[PDF.js Extractor] Extraction complete, text length:', fullText.length);

        if (fullText.trim().length > 50) {
            return fullText.trim();
        }

        throw new Error("PDF appears to be empty");

    } catch (error) {
        console.error('[PDF.js Extractor] Failed:', error);
        throw error;
    }
}
