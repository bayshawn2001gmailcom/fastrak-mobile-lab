<?php
/**
 * Correct Schema Markup — fastrakmobilelab.com
 * Plugin Name: Fastrak Correct Schema
 * Description: Replaces the invalid globally-injected schema block with correct schema
 *              based on what Fastrak Mobile Lab actually is and does.
 * Version: 2.0
 *
 * INSTALLATION:
 *   Upload to: wp-content/mu-plugins/fastrak-correct-schema.php
 *   MU plugins run automatically — no activation needed.
 *
 * ── BUSINESS MODEL (used to determine correct schema type) ───────────────────
 *   Fastrak Mobile Lab is a MOBILE PHLEBOTOMY SERVICE:
 *   - Licensed phlebotomists travel to client's home/office/facility
 *   - Draws blood from a doctor's requisition OR self-pay
 *   - Transports samples to LabCorp or Quest Diagnostics (does NOT own a lab)
 *   - Also collects DNA/paternity testing kits
 *   - Also performs drug testing (pre-employment, DOT, adult entertainment talent)
 *   - Serves busy professionals, elderly, disabled, assisted living facilities
 *
 * ── CORRECT SCHEMA TYPE ──────────────────────────────────────────────────────
 *   @type: "MedicalBusiness"
 *   Rationale:
 *   - MedicalBusiness = "A business for medical purposes run by health professionals"
 *   - Hierarchy: MedicalBusiness → LocalBusiness → Organization (NOT MedicalOrganization)
 *   - NOT DiagnosticLab (they don't run the lab; LabCorp/Quest does)
 *   - NOT MedicalClinic (no fixed patient care location)
 *   - NOT Physician (not a physician practice)
 *
 * ── WHY THE OLD SCHEMA WAS WRONG ─────────────────────────────────────────────
 *   The previous globally-injected block had:
 *   1. @type: ["MedicalBusiness","LocalBusiness"] — redundant; MedicalBusiness IS a LocalBusiness
 *   2. "serviceType": "Mobile Phlebotomy" — serviceType is only valid on schema:Service, not MedicalBusiness
 *   3. "medicalSpecialty": "https://schema.org/LaboratoryScience" — medicalSpecialty is only
 *      valid on Hospital/MedicalClinic/MedicalOrganization/Physician; MedicalBusiness
 *      inherits from LocalBusiness, NOT MedicalOrganization
 *   Source: schema.org/medicalSpecialty, schema.org/serviceType, schema.org/MedicalBusiness
 *
 * ── WHERE serviceType BELONGS ────────────────────────────────────────────────
 *   serviceType is valid on schema:Service — use it there on individual service pages:
 *   { "@type": "Service", "serviceType": "Mobile Phlebotomy", "provider": { "@type": "MedicalBusiness" ... } }
 *
 * ── FAQ SCHEMA NOTE (May 2026) ────────────────────────────────────────────────
 *   Google deprecated FAQ rich results on May 7, 2026. FAQ schema now only generates
 *   rich results for well-known government or health authority sites. Keep FAQPage
 *   schema on the FAQ page (doesn't hurt, helps Google understand content) but
 *   don't expect rich result snippets in SERPs.
 *
 * REMOVE THIS PLUGIN WHEN:
 *   The source PHP function in functions.php is fixed directly.
 *   Search for "serviceType" or "LaboratoryScience" in your theme's functions.php
 *   to find and fix it at the source.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Remove the old invalid globally-injected schema block via output buffering.
 * The Rank Math @graph block (added separately) is correct and should remain.
 */
add_action( 'init', function () {
    ob_start( 'fastrak_replace_invalid_schema' );
} );

function fastrak_replace_invalid_schema( string $output ): string {
    // Skip non-HTML contexts
    if ( is_admin() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
        return $output;
    }

    // Only process if the bad schema is present (short-circuit for performance)
    if ( strpos( $output, '"serviceType"' ) === false ) {
        return $output;
    }

    // Remove the entire bad schema block (standalone LocalBusiness block with invalid fields).
    // Pattern targets the specific block structure output by the custom function.
    // The Rank Math @graph block uses "@graph" and is NOT affected.
    $output = preg_replace(
        '/<script\s+type=["\']application\/ld\+json["\']\s*>\s*\{[^<]*?"serviceType"[^<]*?\}\s*<\/script>\s*/s',
        '',
        $output
    );

    return $output;
}

/**
 * Output the CORRECT MedicalBusiness schema in its place.
 * Hooked at wp_head priority 5 (before Rank Math at priority 10).
 *
 * This outputs the business-level schema only.
 * Service-level schema (with serviceType) should be added per service/city page
 * using Rank Math's custom schema feature or via the service page templates.
 */
add_action( 'wp_head', 'fastrak_output_correct_business_schema', 5 );

function fastrak_output_correct_business_schema(): void {
    // Only output on frontend
    if ( is_admin() ) {
        return;
    }

    $schema = [
        '@context' => 'https://schema.org',
        '@type'    => 'MedicalBusiness',
        'name'     => 'Fastrak Mobile Lab',
        'alternateName' => 'FASTRAK Mobile Lab',
        'description' => 'Mobile phlebotomy service serving Metro Atlanta and Gwinnett County. '
            . 'Licensed phlebotomists travel to your home, office, or facility for blood draws, '
            . 'DNA/paternity testing, and drug testing. Samples delivered to LabCorp or Quest Diagnostics.',
        'url'       => 'https://fastrakmobilelab.com',
        'telephone' => '+16785625244',
        'email'     => 'info@fastrakmobilelab.com',
        'address'   => [
            '@type'           => 'PostalAddress',
            'streetAddress'   => '2330 Scenic Hwy S',
            'addressLocality' => 'Snellville',
            'addressRegion'   => 'GA',
            'postalCode'      => '30078',
            'addressCountry'  => 'US',
        ],
        'geo' => [
            '@type'     => 'GeoCoordinates',
            'latitude'  => 33.84858,
            'longitude' => -84.02493,
        ],
        'areaServed' => [
            [ '@type' => 'City', 'name' => 'Atlanta',        'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Snellville',     'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Lawrenceville',  'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Lilburn',        'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Duluth',         'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Norcross',       'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Tucker',         'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Decatur',        'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Stone Mountain', 'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Conyers',        'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Marietta',       'addressRegion' => 'GA' ],
            [ '@type' => 'City', 'name' => 'Sandy Springs',  'addressRegion' => 'GA' ],
            [ '@type' => 'AdministrativeArea', 'name' => 'Gwinnett County', 'addressRegion' => 'GA' ],
            [ '@type' => 'AdministrativeArea', 'name' => 'Metro Atlanta',   'addressRegion' => 'GA' ],
        ],
        'openingHoursSpecification' => [
            [
                '@type'      => 'OpeningHoursSpecification',
                'dayOfWeek'  => [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday' ],
                'opens'      => '08:00',
                'closes'     => '17:00',
            ],
        ],
        'priceRange' => '$$',
        'image'      => 'https://fastrakmobilelab.com/wp-content/uploads/2025/09/Fastrak-Logo-2-1.webp',
        'sameAs'     => [
            // Add your verified social/directory profiles here:
            // 'https://www.facebook.com/fastrakmobilelab',
            // 'https://www.instagram.com/fastrakmobilelab',
            // 'https://g.page/fastrakmobilelab',
        ],
    ];

    echo '<script type="application/ld+json">' . "\n";
    echo wp_json_encode( $schema, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
    echo "\n" . '</script>' . "\n";
}
