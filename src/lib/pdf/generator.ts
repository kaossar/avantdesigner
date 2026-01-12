import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export async function generatePdf(elementId: string, fileName: string = 'rapport-analyse.pdf') {
    const element = document.getElementById(elementId);
    if (!element) {
        throw new Error(`Element with id ${elementId} not found`);
    }

    try {
        // 1. Capture the element as a canvas
        const canvas = await html2canvas(element, {
            scale: 2, // Higher scale for better resolution
            useCORS: true, // Handle images from other domains if needed
            logging: false,
            backgroundColor: '#ffffff'
        });

        // 2. Initialize PDF
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        });

        // 3. Calculate dimensions
        const imgWidth = 210; // A4 width in mm
        const pageHeight = 297; // A4 height in mm
        const imgHeight = (canvas.height * imgWidth) / canvas.width;

        let heightLeft = imgHeight;
        let position = 0;

        // 4. Add image to PDF (handling multiple pages if long)
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            pdf.addPage();
            pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
        }

        // 5. Save
        pdf.save(fileName);
        return true;

    } catch (error) {
        console.error('Error generating PDF:', error);
        throw error;
    }
}
